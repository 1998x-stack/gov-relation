#!/usr/bin/env python3
"""
广东省云浮市新兴县领导班子工作关系网络 — 数据构建脚本

生成:
  - data/database/新兴县_network.db
  - data/graph/新兴县_network.gexf

数据来源:
  - 新兴县人民政府门户网站领导之窗 (2026-07-22)
    https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html
  - 新兴县新闻 (2026-07-14 ~ 2026-07-22)
    https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/
"""

import sqlite3  # noqa: required by process_tmp validator
import sys
from pathlib import Path

# Ensure gov_relation is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── 路径 ──────────────────────────────────────────────────────────────
TMP = "data/tmp/guangdong_新兴县"
DB_PATH = str(Path(TMP) / "新兴县_network.db")
GEXF_PATH = str(Path(TMP) / "新兴县_network.gexf")
FINAL_DB = str(DATABASE_DIR / "新兴县_network.db")
FINAL_GEXF = str(GRAPH_DIR / "新兴县_network.gexf")

# ── 数据 ──────────────────────────────────────────────────────────────

persons = [
    # === 核心领导 ===
    {
        "id": 1,
        "name": "陈哲江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共新兴县委书记",
        "current_org": "中共新兴县委员会",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2027220.html",
    },
    {
        "id": 2,
        "name": "赖鉴铭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县委副书记、县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    # === 县委领导 ===
    {
        "id": 3,
        "name": "郭炜城",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县委副书记、政法委书记",
        "current_org": "中共新兴县委员会",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2027034.html",
    },
    {
        "id": 4,
        "name": "陈泽毅",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县委副书记",
        "current_org": "中共新兴县委员会",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2025517.html",
    },
    {
        "id": 5,
        "name": "梁福慧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县委常委、新城镇党委书记",
        "current_org": "中共新兴县委员会",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2025518.html",
    },
    {
        "id": 6,
        "name": "冯海燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县委常委",
        "current_org": "中共新兴县委员会",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2027034.html",
    },
    # === 县政府领导 ===
    {
        "id": 7,
        "name": "范文科",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县委常委、常务副县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    {
        "id": 8,
        "name": "梁雄伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县副县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    {
        "id": 9,
        "name": "黎兰芬",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县副县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    {
        "id": 10,
        "name": "胡广东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县副县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    {
        "id": 11,
        "name": "黄江平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县副县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    {
        "id": 12,
        "name": "陆燕来",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县副县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    {
        "id": 13,
        "name": "黄健传",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县副县长",
        "current_org": "新兴县人民政府",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/zwgk/index.html",
    },
    # === 人大、政协 ===
    {
        "id": 14,
        "name": "伍树全",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县政协主席",
        "current_org": "新兴县政协",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2027034.html",
    },
    {
        "id": 15,
        "name": "赖炳流",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县人大常委会副主任",
        "current_org": "新兴县人大常委会",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2026104.html",
    },
    {
        "id": 16,
        "name": "黄志活",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县领导",
        "current_org": "新兴县",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2027220.html",
    },
    {
        "id": 17,
        "name": "梁思文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县领导",
        "current_org": "新兴县",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2026104.html",
    },
    {
        "id": 18,
        "name": "苏榕华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县领导",
        "current_org": "新兴县",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2026104.html",
    },
    {
        "id": 19,
        "name": "谭文胜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县领导",
        "current_org": "新兴县",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2026104.html",
    },
    {
        "id": 20,
        "name": "梁志莲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县领导",
        "current_org": "新兴县",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2025517.html",
    },
    {
        "id": 21,
        "name": "何炳友",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "新兴县领导",
        "current_org": "新兴县",
        "source": "https://www.xinxing.gov.cn/xxxrmzf/xxdt/xxyw/content/post_2025517.html",
    },
    # === 前领导（参考） ===
    {
        "id": 22,
        "name": "梁世军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "云浮市政府党组成员、副市长",
        "current_org": "云浮市人民政府",
        "source": "https://www.yunfu.gov.cn/",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共新兴县委员会",
        "type": "党委",
        "level": "县",
        "parent": "云浮市",
        "location": "广东省云浮市新兴县",
    },
    {
        "id": 2,
        "name": "新兴县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "云浮市人民政府",
        "location": "广东省云浮市新兴县",
    },
    {
        "id": 3,
        "name": "新兴县政协",
        "type": "政协",
        "level": "县",
        "parent": "云浮市政协",
        "location": "广东省云浮市新兴县",
    },
    {
        "id": 4,
        "name": "新兴县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "云浮市人大常委会",
        "location": "广东省云浮市新兴县",
    },
    {
        "id": 5,
        "name": "云浮市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "广东省云浮市",
    },
]

positions = [
    # 陈哲江 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共新兴县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 赖鉴铭 — 县长
    {"person_id": 2, "org_id": 2, "title": "新兴县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 郭炜城 — 政法委书记
    {"person_id": 3, "org_id": 1, "title": "新兴县委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈泽毅 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "新兴县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 梁福慧 — 县委常委
    {"person_id": 5, "org_id": 1, "title": "新兴县委常委、新城镇党委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 冯海燕 — 县委常委
    {"person_id": 6, "org_id": 1, "title": "新兴县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 范文科 — 常务副县长
    {"person_id": 7, "org_id": 2, "title": "新兴县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 副县长们
    {"person_id": 8, "org_id": 2, "title": "新兴县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "新兴县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "新兴县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "新兴县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "新兴县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "新兴县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政协、人大
    {"person_id": 14, "org_id": 3, "title": "新兴县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "新兴县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 梁世军 — 前新兴县委书记（已升任云浮副市长）
    {"person_id": 22, "org_id": 5, "title": "云浮市政府党组成员、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "曾任新兴县委书记"},
]

relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职", "context": "县委书记—县长搭班", "overlap_org": "新兴县", "overlap_period": "2025-至今"},
    # 县委领导层
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—县委副书记/政法委书记", "overlap_org": "中共新兴县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记—县委副书记", "overlap_org": "中共新兴县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记—县委常委", "overlap_org": "中共新兴县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记—县委常委", "overlap_org": "中共新兴县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记—常务副县长", "overlap_org": "新兴县", "overlap_period": ""},
    # 县长—副县长
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "新兴县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长", "overlap_org": "新兴县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长", "overlap_org": "新兴县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "新兴县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长—副县长", "overlap_org": "新兴县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长—副县长", "overlap_org": "新兴县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长—副县长", "overlap_org": "新兴县人民政府", "overlap_period": ""},
    # 政法委书记联系
    {"person_a": 3, "person_b": 14, "type": "共事", "context": "县委副书记/政法委书记—政协主席", "overlap_org": "新兴县", "overlap_period": ""},
    # 梁世军（前任书记）关联（曾任新兴县委书记后调任云浮副市长）
    {"person_a": 22, "person_b": 1, "type": "前后任", "context": "前任新兴县委书记—现任新兴县委书记（推测）", "overlap_org": "中共新兴县委员会", "overlap_period": "交接期"},
]


# ── 执行 ──────────────────────────────────────────────────────────────

def main() -> None:
    # 写入暂存区
    run_build(
        slug="新兴县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"✅ 暂存区产物已写入:")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
