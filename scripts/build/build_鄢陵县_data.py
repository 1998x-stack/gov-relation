#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 鄢陵县 leadership network.

调查日期: 2026-08-05
信息来源: 鄢陵县人民政府门户网站 (www.yanling.gov.cn 政府领导/政务动态/县党代会/县人代会)
调查级别: 县
目标人物: 县委书记 袁树林、县长 田秀杰
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
# 脚本可能位于 data/tmp/<task_id>/（暂存）或 scripts/build/（归档）。
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

STAGING_DIR = str(Path(__file__).resolve().parent)
DB_PATH = os.path.join(STAGING_DIR, "鄢陵县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "鄢陵县_network.gexf")

SLUG = "河南省许昌市鄢陵县"

# ── 官方来源 URL 常量 (供 persons 引用) ────────────────────────────
GOV_LEADERS = "http://www.yanling.gov.cn/ggfw/004008/secondPageLeaders.html"
NEWS_SHUJI_0428 = "http://www.yanling.gov.cn/zwdt/002001/20260428/e913a3fd-f7f1-4acc-9e9e-96faebc78b82.html"
NEWS_XIANZHANG_0513 = "http://www.yanling.gov.cn/zwdt/002001/20260513/59e33be2-f70b-46e7-8c43-681d77da0772.html"
NEWS_CHANGWEI_0727 = "http://www.yanling.gov.cn/zwdt/002001/20260727/eb62c8b8-eaea-4a7d-b15d-4e5534fcecc.html"
NEWS_RENDA_0525 = "http://www.yanling.gov.cn/zwdt/002001/20260525/5cf3df88-cb9e-47d3-945b-12f3d51d32f1.html"
NEWS_ZHENGXIE_0522 = "http://www.yanling.gov.cn/zwdt/002001/20260522/5c7ee88c-7c44-41ce-8a7f-2df52deafe18.html"
NEWS_GOV_0801 = "http://www.yanling.gov.cn/zwdt/002001/20260801/634aa55f-e69a-47cb-981d-f3ac8fa96373.html"

# ── ORGANIZATIONS ─────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鄢陵县委员会", "type": "党委", "level": "县处级", "parent": "中共许昌市委", "location": "河南省许昌市鄢陵县", "source": "http://www.yanling.gov.cn/"},
    {"id": 2, "name": "鄢陵县人民政府", "type": "政府", "level": "县处级", "parent": "许昌市人民政府", "location": "河南省许昌市鄢陵县", "source": GOV_LEADERS},
    {"id": 3, "name": "鄢陵县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "河南省许昌市鄢陵县", "source": NEWS_RENDA_0525},
    {"id": 4, "name": "中国人民政治协商会议鄢陵县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "河南省许昌市鄢陵县", "source": NEWS_ZHENGXIE_0522},
    {"id": 5, "name": "鄢陵县公安局", "type": "政府", "level": "乡科级", "parent": "鄢陵县人民政府", "location": "河南省许昌市鄢陵县", "source": GOV_LEADERS},
]

# ── PERSONS ────────────────────────────────────────────────────────
# 依据: 十五届县委常委会第四次会议 (2026-07-27) 列名的县委常委及列席县领导、
# 县十五次党代会 (2026-06-23)、县十六届人大第六次会议 (2026-05-23)、
# 县政协十届五次会议 (2026-05-21)、县政府领导页 (2026-06-18)。
# 说明: 部分常委的具体分管岗位（组织/宣传/纪委）未从公开渠道逐项核实，留空并列入 open_questions。
persons = [
    # ═══ 县委领导 (Party Committee) ═══
    {
        "id": 1, "name": "袁树林", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共鄢陵县委书记",
        "current_org": "中共鄢陵县委员会",
        "source": NEWS_SHUJI_0428,
    },
    {
        "id": 2, "name": "田秀杰", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年2月", "birthplace": "", "education": "大学学历，法学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "鄢陵县人民政府",
        "source": GOV_LEADERS,
    },
    {
        "id": 3, "name": "杨振华", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县委政法委书记",
        "current_org": "鄢陵县委员会",
        "source": NEWS_CHANGWEI_0727,
    },
    {
        "id": 4, "name": "蒋涛", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "鄢陵县人民代表大会常务委员会",
        "source": NEWS_RENDA_0525,
    },
    {
        "id": 5, "name": "张智勇", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议鄢陵县委员会",
        "source": NEWS_ZHENGXIE_0522,
    },
    {
        "id": 6, "name": "梅雪艳", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共鄢陵县委员会",
        "source": NEWS_CHANGWEI_0727,
    },
    {
        "id": 7, "name": "苗东红", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共鄢陵县委员会",
        "source": NEWS_CHANGWEI_0727,
    },
    {
        "id": 8, "name": "王晓东", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县委统战部部长、县政协党组副书记",
        "current_org": "中共鄢陵县委员会",
        "source": NEWS_ZHENGXIE_0522,
    },
    {
        "id": 9, "name": "陈孟磊", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共鄢陵县委员会",
        "source": NEWS_CHANGWEI_0727,
    },
    {
        "id": 10, "name": "文剑锋", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年4月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县政府常务副县长、党组副书记",
        "current_org": "鄢陵县人民政府",
        "source": GOV_LEADERS,
    },
    {
        "id": 11, "name": "琚晓飞", "gender": "", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共鄢陵县委员会",
        "source": NEWS_CHANGWEI_0727,
    },
    {
        "id": 12, "name": "张文茂", "gender": "男", "ethnicity": "汉族",
        "birth": "1990年2月", "birthplace": "", "education": "研究生，硕士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "鄢陵县人民政府",
        "source": GOV_LEADERS,
    },
    # ═══ 县政府领导 ═══
    {
        "id": 13, "name": "邢千里", "gender": "男", "ethnicity": "汉族",
        "birth": "1981年1月", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府副县长、公安局局长",
        "current_org": "鄢陵县公安局",
        "source": GOV_LEADERS,
    },
    {
        "id": 14, "name": "王志勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年8月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "鄢陵县人民政府",
        "source": GOV_LEADERS,
    },
    {
        "id": 15, "name": "贾腾", "gender": "男", "ethnicity": "汉族",
        "birth": "1987年12月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "鄢陵县人民政府",
        "source": GOV_LEADERS,
    },
    {
        "id": 16, "name": "李小云", "gender": "女", "ethnicity": "汉族",
        "birth": "1986年2月", "birthplace": "", "education": "研究生，硕士学位",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "鄢陵县人民政府",
        "source": GOV_LEADERS,
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 县委核心
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-04-28", "end_date": "至今", "rank": "正处级", "note": "2026-04-28 任中共鄢陵县委书记; 此前任鄢陵县长"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start_date": "约2021/2022", "end_date": "2026-04", "rank": "正处级", "note": "2026-04-22 政府常务会议仍以县长身份; 2026-05-12 起不再担任县长"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-05", "end_date": "至今", "rank": "正处级", "note": "2026-05-12 提名为县长候选人; 2026-05-23 县第十六届人大第六次会议当选"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-05", "end_date": "至今", "rank": "县处级", "note": "县委副书记、代县长/县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "至今", "rank": "县处级", "note": "县委副书记、县委政法委书记"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "县十六届人大第六次会议主席团常务主席、主持并致闭幕词"},
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "县政协十届五次会议作常委会报告"},
    # 县委常委会成员（兼政府）
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "至今", "rank": "县处级", "note": "县政协党组副书记"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": "分管岗位未从公开渠道确认"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县政府常务副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "负责常务工作"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 县政府副县长
    {"person_id": 13, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "县公安局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼任; 县委政法委员会副书记"},
    {"person_id": 14, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "领导关系", "context": "县委书记与县长搭档; 袁树林任书记后田秀杰接任县长", "overlap_org": "鄢陵县委员会", "overlap_period": "2026-05 - 至今"},
    {"person_a": 1, "person_b": 3, "type": "领导关系", "context": "县委书记与县委副书记(政法委书记)", "overlap_org": "中共鄢陵县委员会", "overlap_period": "2026 - 至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记与县人大常委会主任同现人代会主席台", "overlap_org": "鄢陵县人民代表大会常务委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记到会祝贺县政协会议并发表讲话", "overlap_org": "中国人民政治协商会议鄢陵县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "鄢陵县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长与副县长兼公安局长", "overlap_org": "鄢陵县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与副县长(常委)", "overlap_org": "鄢陵县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "县长与副县长", "overlap_org": "鄢陵县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "县长与副县长", "overlap_org": "鄢陵县人民政府", "overlap_period": "至今"},
    {"person_a": 10, "person_b": 12, "type": "同僚", "context": "常务副县长与副县长、县委常委", "overlap_org": "鄢陵县人民政府", "overlap_period": "至今"},
    {"person_a": 13, "person_b": 3, "type": "工作交集", "context": "副县长兼公安局长为县委政法委副书记，受县委副书记/政法委书记领导", "overlap_org": "中共鄢陵县委员会", "overlap_period": "至今"},
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