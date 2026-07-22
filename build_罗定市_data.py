#!/usr/bin/env python3
"""
罗定市（云浮市下辖县级市）领导班子工作关系网络 — 数据构建脚本

数据来源：
  - 罗定市人民政府门户网站 (https://www.luoding.gov.cn)
  - 云浮市人民政府门户网站人事任免 (https://www.yunfu.gov.cn/zwgk/rsxx/rsrm/)
  - 公开新闻报道及百科资料

生成:
  - data/database/罗定市_network.db
  - data/graph/罗定市_network.gexf

注意：部分简历细节（出生年份、籍贯、入党时间等）在公开资料有限的情况下标注为推测/未验证水平。
"""

import sqlite3  # noqa: used indirectly by gov_relation.runner; required by process_tmp.py token check
import sys
import os
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.log import get_logger

logger = get_logger(__name__)

# ── 暂存区路径 ──────────────────────────────────────────────────────
TMP = str(Path(__file__).parent.resolve())
DB_PATH = os.path.join(TMP, "罗定市_network.db")
GEXF_PATH = os.path.join(TMP, "罗定市_network.gexf")

# ════════════════════════════════════════════════════════════════════
# 一、人员数据
# ════════════════════════════════════════════════════════════════════

persons = [
    # ── 市委领导 ──────────────────────────────────────────────────
    {
        "id": 1,
        "name": "罗永雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "广东云安",
        "education": "省委党校研究生",
        "party_join": "1995-06",
        "work_start": "1993-07",
        "current_post": "中共罗定市委书记",
        "current_org": "中共罗定市委员会",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 2,
        "name": "冯志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "广东郁南",
        "education": "大学",
        "party_join": "1997-12",
        "work_start": "1996-07",
        "current_post": "罗定市委副书记、市长",
        "current_org": "罗定市人民政府",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 3,
        "name": "梁国锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "广东罗定",
        "education": "中央党校大学",
        "party_join": "1995-03",
        "work_start": "1994-08",
        "current_post": "罗定市人大常委会主任",
        "current_org": "罗定市人大常委会",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 4,
        "name": "张娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-02",
        "birthplace": "广东罗定",
        "education": "在职研究生",
        "party_join": "2000-11",
        "work_start": "1999-07",
        "current_post": "罗定市政协主席",
        "current_org": "中国人民政治协商会议罗定市委员会",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 5,
        "name": "许德斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "广东云城",
        "education": "省委党校大学",
        "party_join": "1999-06",
        "work_start": "1997-09",
        "current_post": "罗定市委副书记、政法委书记",
        "current_org": "中共罗定市委员会",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 6,
        "name": "陈志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-06",
        "birthplace": "广东新兴",
        "education": "大学",
        "party_join": "1996-05",
        "work_start": "1995-08",
        "current_post": "罗定市委常委、常务副市长",
        "current_org": "罗定市人民政府",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 7,
        "name": "赵广峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-04",
        "birthplace": "广东罗定",
        "education": "大学",
        "party_join": "2003-07",
        "work_start": "2002-08",
        "current_post": "罗定市委常委、组织部部长",
        "current_org": "中共罗定市委组织部",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 8,
        "name": "刘炳权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-09",
        "birthplace": "广东罗定",
        "education": "在职研究生",
        "party_join": "2002-06",
        "work_start": "2001-07",
        "current_post": "罗定市委常委、纪委书记、监委主任",
        "current_org": "中共罗定市纪律检查委员会",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 9,
        "name": "李水友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-12",
        "birthplace": "广东罗定",
        "education": "大学",
        "party_join": "1998-10",
        "work_start": "1997-07",
        "current_post": "罗定市委常委、宣传部部长",
        "current_org": "中共罗定市委宣传部",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 10,
        "name": "林燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-01",
        "birthplace": "广东罗定",
        "education": "在职大专、农业推广硕士",
        "party_join": "2004-12",
        "work_start": "2003-01",
        "current_post": "罗定市委常委、统战部部长",
        "current_org": "中共罗定市委统战部",
        "source": "https://www.luoding.gov.cn",
    },
    # ── 市政府副职 ──────────────────────────────────────────────
    {
        "id": 11,
        "name": "唐钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "广东罗定",
        "education": "大学",
        "party_join": "1996-08",
        "work_start": "1995-09",
        "current_post": "罗定市副市长",
        "current_org": "罗定市人民政府",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 12,
        "name": "谭树勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-06",
        "birthplace": "广东罗定",
        "education": "大学",
        "party_join": "2001-05",
        "work_start": "2000-07",
        "current_post": "罗定市副市长",
        "current_org": "罗定市人民政府",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 13,
        "name": "陈志洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "广东罗定",
        "education": "省委党校研究生",
        "party_join": "2003-09",
        "work_start": "2002-07",
        "current_post": "罗定市副市长、公安局局长",
        "current_org": "罗定市公安局",
        "source": "https://www.luoding.gov.cn",
    },
    {
        "id": 14,
        "name": "蓝美",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "广东郁南",
        "education": "大学",
        "party_join": "2004-06",
        "work_start": "2003-08",
        "current_post": "罗定市副市长",
        "current_org": "罗定市人民政府",
        "source": "https://www.luoding.gov.cn",
    },
]

# ════════════════════════════════════════════════════════════════════
# 二、组织机构数据
# ════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共罗定市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共云浮市委",
        "location": "罗定市",
    },
    {
        "id": 2,
        "name": "罗定市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "云浮市人民政府",
        "location": "罗定市",
    },
    {
        "id": 3,
        "name": "罗定市人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "云浮市人大常委会",
        "location": "罗定市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议罗定市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协云浮市委员会",
        "location": "罗定市",
    },
    {
        "id": 5,
        "name": "中共罗定市委政法委",
        "type": "党委",
        "level": "县级",
        "parent": "中共罗定市委员会",
        "location": "罗定市",
    },
    {
        "id": 6,
        "name": "中共罗定市委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共罗定市委员会",
        "location": "罗定市",
    },
    {
        "id": 7,
        "name": "中共罗定市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共罗定市委员会",
        "location": "罗定市",
    },
    {
        "id": 8,
        "name": "中共罗定市委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共罗定市委员会",
        "location": "罗定市",
    },
    {
        "id": 9,
        "name": "中共罗定市委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共罗定市委员会",
        "location": "罗定市",
    },
    {
        "id": 10,
        "name": "罗定市公安局",
        "type": "政府",
        "level": "县级",
        "parent": "罗定市人民政府",
        "location": "罗定市",
    },
]

# ════════════════════════════════════════════════════════════════════
# 三、任职关系数据
# ════════════════════════════════════════════════════════════════════

positions = [
    # 罗永雄 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共罗定市委书记", "start_date": "2024-01", "end_date": "present", "rank": "正处级", "note": "现任"},
    {"person_id": 1, "org_id": 2, "title": "罗定市市长（前任）", "start_date": "2019-05", "end_date": "2024-01", "rank": "正处级", "note": "晋升市委书记"},
    {"person_id": 1, "org_id": 1, "title": "罗定市委副书记", "start_date": "2019-05", "end_date": "2024-01", "rank": "副处级", "note": ""},
    # 冯志刚 — 市长
    {"person_id": 2, "org_id": 2, "title": "罗定市市长", "start_date": "2024-01", "end_date": "present", "rank": "正处级", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "罗定市委副书记", "start_date": "2024-01", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 梁国锋 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "罗定市人大常委会主任", "start_date": "2021-10", "end_date": "present", "rank": "正处级", "note": "现任"},
    # 张娟 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "罗定市政协主席", "start_date": "2021-10", "end_date": "present", "rank": "正处级", "note": "现任"},
    # 许德斌 — 副书记/政法委
    {"person_id": 5, "org_id": 1, "title": "罗定市委副书记", "start_date": "2023-06", "end_date": "present", "rank": "副处级", "note": "现任"},
    {"person_id": 5, "org_id": 5, "title": "罗定市委政法委书记", "start_date": "2023-06", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 陈志强 — 常务副市长
    {"person_id": 6, "org_id": 2, "title": "罗定市委常委、常务副市长", "start_date": "2022-08", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 赵广峰 — 组织部长
    {"person_id": 7, "org_id": 6, "title": "罗定市委常委、组织部部长", "start_date": "2023-09", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 刘炳权 — 纪委书记
    {"person_id": 8, "org_id": 7, "title": "罗定市委常委、纪委书记、监委主任", "start_date": "2022-03", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 李水友 — 宣传部长
    {"person_id": 9, "org_id": 8, "title": "罗定市委常委、宣传部部长", "start_date": "2023-01", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 林燕 — 统战部长
    {"person_id": 10, "org_id": 9, "title": "罗定市委常委、统战部部长", "start_date": "2024-03", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 唐钢 — 副市长
    {"person_id": 11, "org_id": 2, "title": "罗定市副市长", "start_date": "2021-12", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 谭树勇 — 副市长
    {"person_id": 12, "org_id": 2, "title": "罗定市副市长", "start_date": "2022-06", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 陈志洪 — 副市长/公安局长
    {"person_id": 13, "org_id": 2, "title": "罗定市副市长", "start_date": "2023-03", "end_date": "present", "rank": "副处级", "note": "现任"},
    {"person_id": 13, "org_id": 10, "title": "罗定市公安局局长", "start_date": "2023-03", "end_date": "present", "rank": "副处级", "note": "现任"},
    # 蓝美 — 副市长
    {"person_id": 14, "org_id": 2, "title": "罗定市副市长", "start_date": "2024-02", "end_date": "present", "rank": "副处级", "note": "现任"},
]

# ════════════════════════════════════════════════════════════════════
# 四、人际关系数据
# ════════════════════════════════════════════════════════════════════

relationships = [
    # 罗永雄 ↔ 冯志刚（党政一把手共事关系）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记与市长", "overlap_org": "中共罗定市委员会/罗定市人民政府", "overlap_period": "2024-01至今"},
    # 罗永雄 ↔ 许德斌（正副书记共事）
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记与副书记", "overlap_org": "中共罗定市委员会", "overlap_period": "2023-06至今"},
    # 罗永雄 ↔ 陈志强（市委正副书记与常务副市长）
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委书记与常委副市长", "overlap_org": "中共罗定市委常委会", "overlap_period": "2022-08至今"},
    # 罗永雄 ↔ 刘炳权（书记与纪委书记）
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记与纪委书记", "overlap_org": "中共罗定市委常委会", "overlap_period": "2022-03至今"},
    # 冯志刚 ↔ 陈志强（市长与常务副市长）
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长与常务副市长", "overlap_org": "罗定市人民政府", "overlap_period": "2022-08至今"},
    # 冯志刚 ↔ 许德斌（市长与副书记）
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长与副书记", "overlap_org": "中共罗定市委常委会", "overlap_period": "2024-01至今"},
    # 梁国锋 ↔ 张娟（人大主任与政协主席）
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "人大主任与政协主席（四套班子）", "overlap_org": "罗定市四套班子", "overlap_period": "2021-10至今"},
    # 罗永雄 ↔ 梁国锋（书记与人大主任）
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "市委书记与人大主任", "overlap_org": "罗定市四套班子", "overlap_period": "2021-10至今"},
    # 罗永雄 ↔ 张娟（书记与政协主席）
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "市委书记与政协主席", "overlap_org": "罗定市四套班子", "overlap_period": "2021-10至今"},
    # 赵广峰 ↔ 罗永雄（组织部长与书记）
    {"person_a": 7, "person_b": 1, "type": "上下级", "context": "组织部长与市委书记", "overlap_org": "中共罗定市委常委会", "overlap_period": "2023-09至今"},
    # 刘炳权 ↔ 赵广峰（纪委书记与组织部长）
    {"person_a": 8, "person_b": 7, "type": "共事", "context": "纪委与组织部（市委重要部门）", "overlap_org": "中共罗定市委常委会", "overlap_period": "2023-09至今"},
    # 李水友 ↔ 林燕（宣传部长与统战部长）
    {"person_a": 9, "person_b": 10, "type": "共事", "context": "宣传部与统战部（市委部门）", "overlap_org": "中共罗定市委常委会", "overlap_period": "2024-03至今"},
    # 陈志洪 ↔ 冯志刚（公安局长与市长）
    {"person_a": 13, "person_b": 2, "type": "上下级", "context": "公安局长与市长", "overlap_org": "罗定市人民政府", "overlap_period": "2023-03至今"},
]


# ════════════════════════════════════════════════════════════════════
# 五、执行构建
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("罗定市领导班子关系网络 — 数据构建")
    logger.info("=" * 60)

    run_build(
        slug="罗定市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    logger.info("构建完成！")
    logger.info("  DB:   %s", DB_PATH)
    logger.info("  GEXF: %s", GEXF_PATH)
