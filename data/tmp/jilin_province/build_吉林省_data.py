#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 吉林省领导班子 (Jilin Province Leadership Network).
Investigation date: 2026-07-25
Current 吉林省委书记: 黄强 (as of 2026-06)
Current 吉林省省长: 胡玉亭 (as of 2026-06)
"""

import os
import sqlite3
import sys
from pathlib import Path

# Add repo root to path
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))
os.chdir(str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "吉林省_network.db"
GEXF_PATH = GRAPH_DIR / "吉林省_network.gexf"

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

persons = [
    # ── 黄强 - 吉林省委书记 (Party Secretary) ──
    {"id": 1, "name": "黄强", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-04", "birthplace": "浙江东阳", "education": "西北工业大学管理科学与工程专业博士研究生",
     "party_join": "1983-06", "work_start": "1979-09",
     "current_post": "吉林省委书记", "current_org": "中共吉林省委",
     "source": "https://baike.baidu.com/item/%E9%BB%84%E5%BC%BA/12184428"},

    # ── 胡玉亭 - 吉林省省长 (Governor) ──
    {"id": 2, "name": "胡玉亭", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-07", "birthplace": "山西五台", "education": "北京钢铁学院冶金系钢铁冶金专业大学毕业，工程硕士，教授级高级工程师",
     "party_join": "1986-08", "work_start": "1986-08",
     "current_post": "吉林省委副书记、省长", "current_org": "吉林省人民政府",
     "source": "https://baike.baidu.com/item/%E8%83%A1%E7%8E%89%E4%BA%AD"},

    # ── 刘伟 - 前前任吉林省委书记 (2020-2022)，现任北京市委副书记 ──
    {"id": 3, "name": "刘伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1958-03", "birthplace": "山东滕州", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%88%98%E4%BC%9F/23578613"},

    # ── 景俊海 - 前任吉林省委书记 (2022-2024) ──
    {"id": 4, "name": "景俊海", "gender": "男", "ethnicity": "汉族",
     "birth": "1960-12", "birthplace": "陕西白水", "education": "西北电讯工程学院（现西安电子科技大学）",
     "party_join": "中共党员", "work_start": "1982-07",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E6%99%AF%E4%BF%8A%E6%B5%B7"},

    # ── 韩俊 - 前任吉林省省长 (2023-2024)，现任农业农村部部长 ──
    {"id": 5, "name": "韩俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-11", "birthplace": "山东高青", "education": "西北农林科技大学农业经济管理专业博士",
     "party_join": "中共党员", "work_start": "1989-05",
     "current_post": "农业农村部部长", "current_org": "农业农村部",
     "source": "https://baike.baidu.com/item/%E9%9F%A9%E4%BF%8A"},

    # ── 吴海英 - 吉林省委副书记 ──
    {"id": 6, "name": "吴海英", "gender": "女", "ethnicity": "汉族",
     "birth": "1967-02", "birthplace": "浙江义乌", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委副书记", "current_org": "中共吉林省委",
     "source": "https://baike.baidu.com/item/%E5%90%B4%E6%B5%B7%E8%8B%B1"},

    # ── 史文斌 - 吉林省委常委、省纪委书记 ──
    {"id": 7, "name": "史文斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-12", "birthplace": "江西万载", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委常委、省纪委书记、省监委主任", "current_org": "中共吉林省纪律检查委员会",
     "source": "https://baike.baidu.com/item/%E5%8F%B2%E6%96%87%E6%96%8C"},

    # ── 蔡东 - 吉林省委常委、常务副省长 ──
    {"id": 8, "name": "蔡东", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-10", "birthplace": "山东济南", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委常委、常务副省长", "current_org": "吉林省人民政府",
     "source": "https://baike.baidu.com/item/%E8%94%A1%E4%B8%9C"},

    # ── 张恩惠 - 吉林省委常委、长春市委书记 ──
    {"id": 9, "name": "张恩惠", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-12", "birthplace": "内蒙古托克托", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委常委、长春市委书记", "current_org": "中共长春市委",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E6%81%A9%E6%83%A0"},

    # ── 韩福春 - 吉林省委常委、统战部部长 ──
    {"id": 10, "name": "韩福春", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-02", "birthplace": "吉林长岭", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委常委、统战部部长", "current_org": "中共吉林省委统战部",
     "source": "https://baike.baidu.com/item/%E9%9F%A9%E7%A6%8F%E6%98%A5"},

    # ── 李伟 - 吉林省委常委、宣传部部长 ──
    {"id": 11, "name": "李伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-12", "birthplace": "吉林长春", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委常委、宣传部部长", "current_org": "中共吉林省委宣传部",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E4%BC%9F/23798601"},

    # ── 李明伟 - 吉林省委常委、政法委书记 ──
    {"id": 12, "name": "李明伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-10", "birthplace": "吉林长春", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委常委、政法委书记", "current_org": "中共吉林省委政法委",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%98%8E%E4%BC%9F"},

    # ── 曹路宝 - 吉林省委常委、组织部部长 ──
    {"id": 13, "name": "曹路宝", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-09", "birthplace": "江苏泰州", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省委常委、组织部部长", "current_org": "中共吉林省委组织部",
     "source": "https://baike.baidu.com/item/%E6%9B%B9%E8%B7%AF%E5%AE%9D"},

    # ── 高志国 - 吉林省政协主席 ──
    {"id": 14, "name": "高志国", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-05", "birthplace": "吉林长春", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省政协主席", "current_org": "吉林省政协",
     "source": "https://baike.baidu.com/item/%E9%AB%98%E5%BF%97%E5%9B%BD/22438588"},

    # ── 副省长1: 刘凯 ──
    {"id": 15, "name": "刘凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省副省长", "current_org": "吉林省人民政府",
     "source": "https://baike.baidu.com/item/%E5%88%98%E5%87%AF/23487004"},

    # ── 副省长2: 李国强 ──
    {"id": 16, "name": "李国强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省副省长", "current_org": "吉林省人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E5%9B%BD%E5%BC%BA"},

    # ── 副省长3: 郭灵计 ──
    {"id": 17, "name": "郭灵计", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省副省长", "current_org": "吉林省人民政府",
     "source": "https://baike.baidu.com/item/%E9%83%AD%E7%81%B5%E8%AE%A1"},

    # ── 副省长4: 杨安娣 ──
    {"id": 18, "name": "杨安娣", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吉林省副省长", "current_org": "吉林省人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%A8%E5%AE%89%E5%A8%A3"},

    # ── 副省长5: 梁仁哲 ──
    {"id": 19, "name": "梁仁哲", "gender": "男", "ethnicity": "朝鲜族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吉林省副省长", "current_org": "吉林省人民政府",
     "source": "https://baike.baidu.com/item/%E6%A2%81%E4%BB%81%E5%93%B2"},

    # ── 吉林省人大常委会主任 (通常由省委书记兼任) ──
    {"id": 20, "name": "黄强", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-04", "birthplace": "浙江东阳", "education": "",
     "party_join": "1983-06", "work_start": "1979-09",
     "current_post": "吉林省人大常委会主任", "current_org": "吉林省人大常委会",
     "source": "https://baike.baidu.com/item/%E9%BB%84%E5%BC%BA/12184428"},
]

organizations = [
    {"id": 1, "name": "中共吉林省委", "type": "党委", "level": "省级", "parent": "", "location": "长春"},
    {"id": 2, "name": "吉林省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长春"},
    {"id": 3, "name": "中共吉林省纪律检查委员会", "type": "纪委", "level": "省级", "parent": "中共吉林省委", "location": "长春"},
    {"id": 4, "name": "中共吉林省委组织部", "type": "党委部门", "level": "省级", "parent": "中共吉林省委", "location": "长春"},
    {"id": 5, "name": "中共吉林省委宣传部", "type": "党委部门", "level": "省级", "parent": "中共吉林省委", "location": "长春"},
    {"id": 6, "name": "中共吉林省委统战部", "type": "党委部门", "level": "省级", "parent": "中共吉林省委", "location": "长春"},
    {"id": 7, "name": "中共吉林省委政法委", "type": "党委部门", "level": "省级", "parent": "中共吉林省委", "location": "长春"},
    {"id": 8, "name": "中共长春市委", "type": "党委", "level": "副省级", "parent": "中共吉林省委", "location": "长春"},
    {"id": 9, "name": "吉林省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "长春"},
    {"id": 10, "name": "吉林省政协", "type": "政协", "level": "省级", "parent": "", "location": "长春"},
]

positions = [
    # 黄强
    {"person_id": 1, "org_id": 1, "title": "吉林省委书记", "start_date": "2024-06", "end_date": "present", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "吉林省人大常委会主任", "start_date": "2024-06", "end_date": "present", "rank": "正省级", "note": "通常由省委书记兼任"},
    # 黄强前任经历
    {"person_id": 1, "org_id": 2, "title": "四川省省长", "start_date": "2020-12", "end_date": "2024-06", "rank": "正省级", "note": "前任省长，调任吉林"},
    {"person_id": 1, "org_id": 2, "title": "河南省委副书记、省长", "start_date": "2016-04", "end_date": "2020-12", "rank": "正省级", "note": ""},

    # 胡玉亭
    {"person_id": 2, "org_id": 2, "title": "吉林省省长", "start_date": "2024-04", "end_date": "present", "rank": "正省级", "note": "吉林省委副书记、省长"},
    # 胡玉亭前任经历
    {"person_id": 2, "org_id": 2, "title": "辽宁省委副书记、大连市委书记", "start_date": "2021-10", "end_date": "2024-04", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "山西省委常委、常务副省长", "start_date": "2019-04", "end_date": "2021-10", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "山西省委常委、省委秘书长", "start_date": "2018-01", "end_date": "2019-04", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "太原市市长", "start_date": "2016-07", "end_date": "2018-01", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "太原钢铁（集团）有限公司总经理", "start_date": "2012-01", "end_date": "2016-07", "rank": "正厅级", "note": "企业任职"},

    # 吴海英
    {"person_id": 6, "org_id": 1, "title": "吉林省委副书记", "start_date": "2023-10", "end_date": "present", "rank": "副省级", "note": ""},

    # 史文斌
    {"person_id": 7, "org_id": 3, "title": "吉林省纪委书记、省监委主任", "start_date": "2023-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 蔡东
    {"person_id": 8, "org_id": 2, "title": "吉林省委常委、常务副省长", "start_date": "2022-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 张恩惠
    {"person_id": 9, "org_id": 8, "title": "长春市委书记", "start_date": "2023-04", "end_date": "present", "rank": "副省级", "note": "省委常委兼任"},
    {"person_id": 9, "org_id": 1, "title": "吉林省委常委", "start_date": "2023-04", "end_date": "present", "rank": "副省级", "note": ""},

    # 韩福春
    {"person_id": 10, "org_id": 6, "title": "吉林省委统战部部长", "start_date": "2023-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 李伟
    {"person_id": 11, "org_id": 5, "title": "吉林省委宣传部部长", "start_date": "2023-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 李明伟
    {"person_id": 12, "org_id": 7, "title": "吉林省委政法委书记", "start_date": "2023-04", "end_date": "present", "rank": "副省级", "note": ""},

    # 曹路宝
    {"person_id": 13, "org_id": 4, "title": "吉林省委组织部部长", "start_date": "2023-01", "end_date": "present", "rank": "副省级", "note": ""},

    # 高志国
    {"person_id": 14, "org_id": 10, "title": "吉林省政协主席", "start_date": "2023-01", "end_date": "present", "rank": "正省级", "note": ""},

    # 副省长们
    {"person_id": 15, "org_id": 2, "title": "吉林省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "吉林省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "吉林省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "吉林省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "吉林省副省长", "start_date": "", "end_date": "present", "rank": "副省级", "note": ""},

    # 前任们
    {"person_id": 4, "org_id": 1, "title": "吉林省委书记", "start_date": "2020-11", "end_date": "2024-06", "rank": "正省级", "note": "前任省委书记"},
    {"person_id": 5, "org_id": 2, "title": "吉林省省长", "start_date": "2023-04", "end_date": "2024-04", "rank": "正省级", "note": "前任省长"},
]

relationships = [
    # 黄强 — 胡玉亭（搭班工作）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "省委书记—省长搭班", "overlap_org": "吉林省", "overlap_period": "2024-04至今"},
    # 黄强 — 景俊海（前任继任）
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "接替景俊海任吉林省委书记", "overlap_org": "中共吉林省委", "overlap_period": "2024-06"},
    # 胡玉亭 — 韩俊（前任继任）
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor", "context": "接替韩俊任吉林省省长", "overlap_org": "吉林省人民政府", "overlap_period": "2024-04"},
    # 黄强 — 吴海英（上下级）
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "省委书记—省委副书记", "overlap_org": "中共吉林省委", "overlap_period": "2024-06至今"},
    # 黄强 — 张恩惠（上下级）
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "省委书记—省委常委/长春市委书记", "overlap_org": "中共吉林省委", "overlap_period": "2024-06至今"},
    # 胡玉亭 — 蔡东（上下级）
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "省长—常务副省长", "overlap_org": "吉林省人民政府", "overlap_period": "2024-04至今"},
    # 胡玉亭 — 吴海英（搭班）
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "省委副书记—省长同班子", "overlap_org": "吉林省", "overlap_period": "2024-04至今"},
    # 景俊海 — 韩俊（前任前后任书记省长搭班）
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "前任省委书记—前任省长搭班", "overlap_org": "吉林省", "overlap_period": "2023-04至2024-04"},
]

# ═══════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="吉林省",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done: 吉林省 network built.")
