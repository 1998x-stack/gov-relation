import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "临安区"
TODAY = "2026-07-28"

persons = [
    {
        "id": 1, "name": "惠海涛", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委书记", "current_org": "中共杭州市临安区委",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46778bbdb19aa40e7970.html"
    },
    {
        "id": 2, "name": "沈建", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区长", "current_org": "杭州市临安区人民政府",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46778bbdb19aa40e7970.html"
    },
    {
        "id": 3, "name": "钱美仙", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区人大常委会主任", "current_org": "杭州市临安区人大常委会",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46778bbdb19aa40e7970.html"
    },
    {
        "id": 4, "name": "李赛文", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区政协主席", "current_org": "杭州市临安区政协",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_2a21eb71127548028c8d9efc4b2d0d75.html"
    },
    {
        "id": 5, "name": "汤丽玉", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委副书记", "current_org": "中共杭州市临安区委",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46778bbdb19aa40e7970.html"
    },
    {
        "id": 6, "name": "唐锋", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "杭州市临安区人民政府",
        "source": "https://www.linan.gov.cn/col/col1229299197/art/2026/art_9bed679887e24cc7bfb7b79ff85a89ce.html"
    },
    {
        "id": 7, "name": "陈立群", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "杭州市临安区人民政府",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_7c48b91fc48a44929fa0216c0b5570f1.html"
    },
    {
        "id": 8, "name": "洪亮", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "杭州市临安区人民政府",
        "source": "https://www.linan.gov.cn/col/col1229299197/art/2026/art_9bed679887e24cc7bfb7b79ff85a89ce.html"
    },
    {
        "id": 9, "name": "田江波", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "杭州市临安区人民政府",
        "source": "https://www.linan.gov.cn/col/col1229299197/art/2026/art_9bed679887e24cc7bfb7b79ff85a89ce.html"
    },
    {
        "id": 10, "name": "张凯", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "杭州市临安区人民政府",
        "source": "https://www.linan.gov.cn/col/col1229299197/art/2026/art_9bed679887e24cc7bfb7b79ff85a89ce.html"
    },
    {
        "id": 11, "name": "罗爱芬", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "杭州市临安区人民政府",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_7c48b91fc48a44929fa0216c0b5570f1.html"
    },
    {
        "id": 12, "name": "高吉亚", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "人大常委会副主任", "current_org": "杭州市临安区人大常委会",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"
    },
    {
        "id": 13, "name": "陈国权", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "人大常委会副主任", "current_org": "杭州市临安区人大常委会",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"
    },
    {
        "id": 14, "name": "鲁一成", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "人大常委会副主任", "current_org": "杭州市临安区人大常委会",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"
    },
    {
        "id": 15, "name": "张勤", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "人大常委会副主任", "current_org": "杭州市临安区人大常委会",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"
    },
    {
        "id": 16, "name": "陈栋", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "人大常委会副主任", "current_org": "杭州市临安区人大常委会",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"
    },
    {
        "id": 17, "name": "黄寅", "gender": "", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "人大常委会副主任", "current_org": "杭州市临安区人大常委会",
        "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"
    },
]

organizations = [
    {"id": 1, "name": "中共杭州市临安区委", "type": "党委", "level": "市辖区", "parent": "中共杭州市委", "location": "浙江省杭州市临安区"},
    {"id": 2, "name": "杭州市临安区人民政府", "type": "政府", "level": "市辖区", "parent": "杭州市人民政府", "location": "浙江省杭州市临安区"},
    {"id": 3, "name": "杭州市临安区人大常委会", "type": "人大", "level": "市辖区", "parent": "杭州市人大常委会", "location": "浙江省杭州市临安区"},
    {"id": 4, "name": "杭州市临安区政协", "type": "政协", "level": "市辖区", "parent": "杭州市政协", "location": "浙江省杭州市临安区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正区级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正区级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "正区级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正区级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正区级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "副区级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长主要领导搭档", "overlap_org": "临安区委/区政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "同僚", "context": "区委书记与区委副书记", "overlap_org": "临安区委", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "同僚", "context": "区长与区委副书记", "overlap_org": "临安区委/区政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与副区长", "overlap_org": "临安区政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长与副区长", "overlap_org": "临安区政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长", "overlap_org": "临安区政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长与副区长", "overlap_org": "临安区政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长", "overlap_org": "临安区政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长", "overlap_org": "临安区政府", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 12, "type": "上下级", "context": "人大主任与副主任", "overlap_org": "区人大常委会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 13, "type": "上下级", "context": "人大主任与副主任", "overlap_org": "区人大常委会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 14, "type": "上下级", "context": "人大主任与副主任", "overlap_org": "区人大常委会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 15, "type": "上下级", "context": "人大主任与副主任", "overlap_org": "区人大常委会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 16, "type": "上下级", "context": "人大主任与副主任", "overlap_org": "区人大常委会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 17, "type": "上下级", "context": "人大主任与副主任", "overlap_org": "区人大常委会", "overlap_period": "2026"},
]

run_build(
    slug=SLUG,
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DATABASE_DIR / "临安区_network.db",
    gexf_path=GRAPH_DIR / "临安区_network.gexf",
    data_dir=DATABASE_DIR,
)