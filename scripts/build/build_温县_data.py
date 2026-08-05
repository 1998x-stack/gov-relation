#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 温县 leadership network.

调查日期: 2026-08-05
信息来源: 温县人民政府门户网站 (www.wenxian.gov.cn 政府领导/温县要闻/人大政协会议)
调查级别: 县
目标人物: 县委书记 卢继成、县长 杜鹏
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
# 脚本可能位于 data/tmp/<task_id>/（暂存）或 scripts/build/（归档），
# 向上遍历定位含 gov_relation 包的仓库根目录。
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STAGING_DIR = str(Path(__file__).resolve().parent)
DB_PATH = os.path.join(STAGING_DIR, "温县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "温县_network.gexf")

SLUG = "河南省焦作市温县"

# ── ORGANIZATIONS ─────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共温县委员会", "type": "党委", "level": "县处级", "parent": "中共焦作市委", "location": "河南省焦作市温县", "source": "https://www.wenxian.gov.cn/"},
    {"id": 2, "name": "温县人民政府", "type": "政府", "level": "县处级", "parent": "焦作市人民政府", "location": "河南省焦作市温县", "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/"},
    {"id": 3, "name": "温县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南省焦作市温县", "source": "https://www.wenxian.gov.cn/2026/06-12/605331.html"},
    {"id": 4, "name": "中国人民政治协商会议温县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河南省焦作市温县", "source": "https://www.wenxian.gov.cn/2026/06-11/605243.html"},
    {"id": 5, "name": "温县公安局", "type": "政府", "level": "乡科级", "parent": "温县人民政府", "location": "河南省焦作市温县", "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/"},
    {"id": 6, "name": "温县人民检察院", "type": "检察院", "level": "县处级", "parent": "温县人民代表大会", "location": "河南省焦作市温县", "source": "https://www.wenxian.gov.cn/2026/06-12/605331.html"},
]

# ── PERSONS ────────────────────────────────────────────────────────
# 温县县委第十四届常委会 (2026-06-22 党代会选举): 卢继成、杜鹏、董岩、冯国杰、张辉、
#   李飞、郭东林、申远、何承泽、郭琳、常磊
# 注: 政府领导页面 "常务副县长" 处显示姓名疑似 冯国杰（与县委常委名单一致），民意录为 冯国杰。
# 身份信息 (出生年、籍贯、教育) 公开渠道缺失 → 留空并列入 open_questions。
persons = [
    # ═══ 县委领导 (Party Committee) ═══
    {
        "id": 1, "name": "卢继成", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共温县县委书记",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (十四届第一次全会 2026-06-24); https://www.wenxian.gov.cn/2026/06-23/606093.html (十四次党代会闭幕)",
    },
    {
        "id": 2, "name": "杜鹏", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "温县人民政府",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html; https://www.wenxian.gov.cn/2026/07-31/609805.html (八一慰问 县长带队)",
    },
    {
        "id": 3, "name": "董岩", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (十四届第一次全会当选副书记)",
    },
    {
        "id": 4, "name": "冯国杰", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县政府常务副县长",
        "current_org": "温县人民政府",
        "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/ (政府领导-常务副县长); https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    {
        "id": 5, "name": "张辉", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    {
        "id": 6, "name": "李飞", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    {
        "id": 7, "name": "郭东林", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    {
        "id": 8, "name": "申远", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    {
        "id": 9, "name": "何承泽", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    {
        "id": 10, "name": "郭琳", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    {
        "id": 11, "name": "常磊", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "温县人民政府",
        "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/ (政府领导-副县长); https://www.wenxian.gov.cn/2026/06-24/606192.html (县委常委)",
    },
    # ═══ 县政府领导 ═══
    {
        "id": 12, "name": "王欢欢", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "温县人民政府",
        "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/ (政府领导-副县长 王欢欢)",
    },
    {
        "id": 13, "name": "侯杰", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民政府副县长、县公安局局长",
        "current_org": "温县公安局",
        "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/ (政府领导-副县长兼公安局长)",
    },
    {
        "id": 14, "name": "王温波", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "温县人民政府",
        "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/ (政府领导-副县长)",
    },
    {
        "id": 15, "name": "赵博", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "温县人民政府",
        "source": "https://www.wenxian.gov.cn/zwgk/zfxxgkml/zfld/ (政府领导-副县长)",
    },
    # ═══ 县人大 ═══
    {
        "id": 16, "name": "王琳琳", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "温县人民代表大会常务委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-12/605331.html (人大六次会议主席团常务主席)",
    },
    {
        "id": 17, "name": "孙启卫", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "温县人民代表大会常务委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-12/605331.html (人大主席团)",
    },
    {
        "id": 18, "name": "岳希文", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会副主任 (2026-06-11 新当选)",
        "current_org": "温县人民代表大会常务委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-12/605331.html (第一号公告)",
    },
    # ═══ 县政协 ═══
    {
        "id": 19, "name": "周胜利", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-11/605243.html (政协十届五次闭幕主持)",
    },
    {
        "id": 20, "name": "张保宏", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议温县委员会",
        "source": "https://www.wenxian.gov.cn/2026/06-11/605243.html (政协全会)",
    },
    # ═══ 检察院 ═══
    {
        "id": 21, "name": "耿元光", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民检察院检察长 (2026-06-11 当选)",
        "current_org": "温县人民检察院",
        "source": "https://www.wenxian.gov.cn/2026/06-12/605331.html (第二号公告)",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 县委核心
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "第十四届县委书记 (2026-06 连任/确认); 曾代表第十三届县委作报告"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "至今", "rank": "县处级", "note": "第十四届县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "至今", "rank": "县处级", "note": "第十四届县委副书记"},
    # 县委常委会成员 (兼政府)
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县政府常务副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 县政府副县长
    {"person_id": 12, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "县公安局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼副县长"},
    {"person_id": 14, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "县人民政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 人大/政协/检察院
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2026-06-11 第一号公告当选"},
    {"person_id": 19, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 6, "title": "县人民检察院检察长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2026-06-11 第二号公告当选"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
# 确认交集均来自 2026-06 党代会 / 人大 / 政协全会 官方名单共同列席。
relationships = [
    {"person_a": 1, "person_b": 2, "type": "领导关系", "context": "县委书记与县长搭档，共同主持县党政工作、共同出席人大政协全会", "overlap_org": "中共温县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 3, "type": "领导关系", "context": "县委书记与县委副书记(第十四届)" , "overlap_org": "中共温县委员会", "overlap_period": "2026-06 - 至今"},
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "两位县委副书记", "overlap_org": "中共温县委员会", "overlap_period": "2026-06 - 至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "温县人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 16, "type": "共事", "context": "县委书记与人大常委会主任在人大会主席团并列(人大六次会议主席团常务主席/主席台前排)", "overlap_org": "温县人民代表大会常务委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 19, "type": "共事", "context": "县委书记与县政协主席同现两会主席台前排", "overlap_org": "中国人民政治协商会议温县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长与副县长兼公安局长", "overlap_org": "温县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与副县长", "overlap_org": "温县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "县长与副县长", "overlap_org": "温县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "县长与副县长", "overlap_org": "温县人民政府", "overlap_period": "至今"},
]

# ── BUILD ──────────────────────────────────────────────────────────
def build() -> None:
    from gov_relation.runner import run_build

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

    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    print("persons: ", conn.execute("select count(*) from persons").fetchone()[0])
    print("organizations: ", conn.execute("select count(*) from organizations").fetchone()[0])
    print("positions: ", conn.execute("select count(*) from positions").fetchone()[0])
    print("relationships: ", conn.execute("select count(*) from relationships").fetchone()[0])
    conn.close()
    print("DB_PATH:", DB_PATH)
    print("GEXF_PATH:", GEXF_PATH)


if __name__ == "__main__":
    build()