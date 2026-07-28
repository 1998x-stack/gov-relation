"""海宁市领导班子关系网络 — 县级市构建脚本。

数据来源：
- 海宁市人民政府网站 (haining.gov.cn) 领导之窗页面 — 2026年7月确认
- 市长之窗各领导简历页面 — 2026年7月确认
- 海宁日报/大潮新闻报道 — 徐明良、滕鸣娅多次出镜确认
- 政务活动新闻 — 市委常委会成员名单

数据时效：2026-07-28
"""

import sys
from pathlib import Path

# 将项目根目录加入路径
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import sqlite3  # noqa: used by run_build internally

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "海宁市"
STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "海宁市_network.db"
GEXF_PATH = STAGING_DIR / "海宁市_network.gexf"

# ═══════════════════════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════════════════════
PERSONS = [
    # ── 市委书记 ──
    {
        "id": 1,
        "name": "徐明良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共海宁市委员会",
        "source": "https://www.haining.gov.cn/col/col1229882204/index.html",
        "notes": "多次在2026年7月出席政务活动；主持深改委会议、参加浙大合作会议、慰问一线劳动者",
    },
    # ── 市委副书记、市长 ──
    {
        "id": 2,
        "name": "滕鸣娅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "",
        "education": "大学学历，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "海宁市人民政府",
        "source": "https://www.haining.gov.cn/col/col1649493/index.html",
        "notes": "1980年1月出生",
    },
    # ── 市委常委、常务副市长 ──
    {
        "id": 3,
        "name": "姜生明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "海宁市人民政府",
        "source": "https://www.haining.gov.cn/col/col1229622011/index.html",
    },
    # ── 副市长 ──
    {
        "id": 4,
        "name": "万成兆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "海宁市人民政府",
        "source": "https://www.haining.gov.cn/col/col1649495/index.html",
    },
    # ── 副市长 ──
    {
        "id": 5,
        "name": "马哲峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-01",
        "birthplace": "",
        "education": "大学学历，工程硕士",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "海宁市人民政府",
        "source": "https://www.haining.gov.cn/col/col1649494/index.html",
        "notes": "非中共党员（民建）",
    },
    # ── 副市长 ──
    {
        "id": 6,
        "name": "陈华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-04",
        "birthplace": "",
        "education": "大学学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "海宁市人民政府",
        "source": "https://www.haining.gov.cn/col/col1229560341/index.html",
    },
    # ── 副市长 ──
    {
        "id": 7,
        "name": "章如强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "海宁市人民政府",
        "source": "https://www.haining.gov.cn/col/col1649498/index.html",
    },
    # ── 副市长、市公安局局长 ──
    {
        "id": 8,
        "name": "郭宗敖",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1977-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "海宁市人民政府/海宁市公安局",
        "source": "https://www.haining.gov.cn/col/col1651042/index.html",
    },
    # ── 副市长 ──
    {
        "id": 9,
        "name": "李静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "海宁市人民政府",
        "source": "https://www.haining.gov.cn/col/col1229878861/index.html",
        "notes": "最年轻副市长（1987年出生）",
    },
    # ── 市委常委（已确认） ──
    {
        "id": 10,
        "name": "陆斌峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共海宁市委员会",
        "source": "https://www.haining.gov.cn/",
        "notes": "2026年7月24日作为市委常委带队调研；具体分管待确认",
    },
    # ── 市人大常委会主任 ──
    {
        "id": 11,
        "name": "濮新达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "海宁市人民代表大会常务委员会",
        "source": "https://www.haining.gov.cn/col/col1229519873/art/2026/art_59c11aad032c4c3eb2a67eb28d6ad1d5.html",
    },
    # ── 市委副书记（推测） ──
    {
        "id": 12,
        "name": "应培国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记（推测）",
        "current_org": "中共海宁市委员会",
        "source": "https://www.haining.gov.cn/col/col1229882465/art/2026/art_211f4b93ce5247e39886a36d7c04fbb2.html",
        "notes": "出席深改委会议，列为市领导，具体职务待确认（推测为副书记或政法委书记）",
    },
]

# ═══════════════════════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════════════════════
ORGANIZATIONS = [
    {"id": 1, "name": "中共海宁市委员会", "type": "党委", "level": "县处级"},
    {"id": 2, "name": "海宁市人民政府", "type": "政府", "level": "县处级"},
    {"id": 3, "name": "海宁市公安局", "type": "政府", "level": "乡科级"},
    {"id": 4, "name": "海宁市人民代表大会常务委员会", "type": "人大", "level": "县处级"},
    {"id": 5, "name": "中共海宁市委政法委员会", "type": "党委", "level": "县处级"},
    {"id": 6, "name": "中共海宁市纪律检查委员会", "type": "党委", "level": "县处级"},
]

# ═══════════════════════════════════════════════════════════════
# 任职数据（person_id → org_id, title, period）
# ═══════════════════════════════════════════════════════════════
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present"},
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "", "end_date": "present"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present"},
    {"person_id": 3, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present"},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present"},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present"},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present"},
    {"person_id": 8, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "present"},
    {"person_id": 8, "org_id": 3, "title": "市公安局局长", "start_date": "", "end_date": "present"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present"},
    {"person_id": 11, "org_id": 4, "title": "市人大常委会主任", "start_date": "", "end_date": "present"},
    {"person_id": 12, "org_id": 1, "title": "市委副书记（推测）", "start_date": "", "end_date": "present"},
]

# ═══════════════════════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════════════════════
RELATIONSHIPS = [
    # 徐明良 ↔ 滕鸣娅 — 党政主要领导
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "海宁市党政主要领导，共同出席多次政务活动（浙大合作会议、防汛防台督导等）",
        "overlap_org": "中共海宁市委员会",
        "overlap_period": "2024-至今",
    },
    # 滕鸣娅 — 应培国 — 副书记同僚
    {
        "person_a": 2,
        "person_b": 12,
        "type": "同僚",
        "context": "共同出席深改委会议，均为市委领导",
        "overlap_org": "中共海宁市委员会",
        "overlap_period": "2024-至今",
    },
    # 姜生明 — 徐明良 — 上下级
    {
        "person_a": 3,
        "person_b": 1,
        "type": "上下级",
        "context": "姜生明为市委常委、常务副市长，在徐明良领导下工作",
        "overlap_org": "中共海宁市委员会",
        "overlap_period": "2024-至今",
    },
]

# ═══════════════════════════════════════════════════════════════
# 运行构建
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"✅ {SLUG} 网络数据库和 GEXF 已生成")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")