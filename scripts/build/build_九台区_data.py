#!/usr/bin/env python3
"""Build script for 长春市九台区 (Jiutai District, Changchun City) leadership network.

Data source: http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/ (official government website)
Survey date: 2026-08-03
"""

import sys
import os
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "九台区_network.db"
GEXF_PATH = GRAPH_DIR / "九台区_network.gexf"

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共长春市九台区委员会", "type": "党委", "level": "市辖区", "parent": "中共长春市委", "location": "长春市九台区"},
    {"id": 2, "name": "长春市九台区人民政府", "type": "政府", "level": "市辖区", "parent": "长春市人民政府", "location": "长春市九台区"},
    {"id": 3, "name": "长春市九台区人大常委会", "type": "人大", "level": "市辖区", "parent": "长春市人大常委会", "location": "长春市九台区"},
    {"id": 4, "name": "政协长春市九台区委员会", "type": "政协", "level": "市辖区", "parent": "长春市政协", "location": "长春市九台区"},
    {"id": 5, "name": "长春市公安局九台分局", "type": "政府部门", "level": "市辖区", "parent": "长春市公安局", "location": "长春市九台区"},
]

# ── Persons ──
persons = [
    {"id": 1, "name": "车志昕", "gender": "男", "ethnicity": "汉族", "birth": "1983年3月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "区委副书记、代区长", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202108/t20210804_2879682.html"},
    {"id": 2, "name": "祖东航", "gender": "男", "ethnicity": "汉族", "birth": "1971年5月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、副区长", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202103/t20210308_2768286.html"},
    {"id": 3, "name": "费欣伟", "gender": "男", "ethnicity": "汉族", "birth": "1975年2月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "区委常委、副区长", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202607/t20260730_3503610.html"},
    {"id": 4, "name": "朴英", "gender": "女", "ethnicity": "朝鲜族", "birth": "1975年11月", "birthplace": "", "education": "研究生学历，工商管理硕士（MBA）", "party_join": "民建会员", "work_start": "", "current_post": "副区长", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202501/t20250106_3372787.html"},
    {"id": 5, "name": "秦力民", "gender": "男", "ethnicity": "汉族", "birth": "1973年9月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "副区长、九台区公安分局局长", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202108/t20210818_2888269.html"},
    {"id": 6, "name": "张帆", "gender": "男", "ethnicity": "汉族", "birth": "1988年6月", "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "", "current_post": "副区长", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202109/t20210909_2899007.html"},
    {"id": 7, "name": "罗强华", "gender": "男", "ethnicity": "汉族", "birth": "1982年1月", "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "", "current_post": "副区长", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202504/t20250425_3395708.html"},
    {"id": 8, "name": "郑权", "gender": "男", "ethnicity": "汉族", "birth": "1974年6月", "birthplace": "", "education": "大学学历", "party_join": "中共党员", "work_start": "", "current_post": "区政府党组成员", "current_org": "长春市九台区人民政府", "source": "http://www.jiutai.gov.cn/zwgk/zjzf/ldxx/202504/t20250425_3395711.html"},
    {"id": 9, "name": "陈亮", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区委书记", "current_org": "中共长春市九台区委员会", "source": "http://www.jiutai.gov.cn/"},
    {"id": 10, "name": "张运广", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区人大常委会主任", "current_org": "长春市九台区人大常委会", "source": "http://www.jiutai.gov.cn/dzxx/zyhy/202608/t20260803_3504187.html"},
    {"id": 11, "name": "王晓东", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "区政协主席", "current_org": "政协长春市九台区委员会", "source": "http://www.jiutai.gov.cn/dzxx/zyhy/202607/t20260724_3502589.html"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 2, "title": "代区长", "start_date": "2026", "end_date": "present", "rank": "", "note": "区委副书记、代区长，主持区政府全面工作，分管区审计局"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "2026", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "常务副区长级", "note": "分管发改、财政、人社、应急等"},
    {"person_id": 2, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长", "start_date": "2026-08", "end_date": "present", "rank": "", "note": "分管财政（国企国资）、自然资源、住建、城管等"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "2026-08", "end_date": "present", "rank": "", "note": "经九台区第十九届人大常委会第三十三次会议任命"},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "", "note": "分管教育、文旅、卫健、科技等（民建会员）"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "", "note": "分管公安、司法、退役军人、信访等"},
    {"person_id": 5, "org_id": 5, "title": "局长", "start_date": "", "end_date": "present", "rank": "", "note": "兼任长春市公安局九台分局局长"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "", "note": "分管工信、商务、民政、政务服务等"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "", "note": "分管交通、供销、残联等"},
    {"person_id": 8, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "", "note": "协助副区长祖东航分管农业农村工作"},
    {"person_id": 9, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "", "note": "九台区委主要负责人"},
    {"person_id": 10, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "", "note": ""},
]

# ── Relationships ──
relationships = [
    {"person_a": 9, "person_b": 1, "type": "共事", "context": "区委书记—代区长党政搭档", "overlap_org": "长春市九台区", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区长—常务副区长", "overlap_org": "九台区政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "区长—副区长(区委常委)", "overlap_org": "九台区政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "九台区政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "区长—副区长(公安局长)", "overlap_org": "九台区政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "区长—副区长", "overlap_org": "九台区政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "九台区政府", "overlap_period": "2026-"},
    {"person_a": 9, "person_b": 2, "type": "共事", "context": "区委书记—区委常委", "overlap_org": "九台区委", "overlap_period": ""},
    {"person_a": 9, "person_b": 3, "type": "共事", "context": "区委书记—区委常委", "overlap_org": "九台区委", "overlap_period": "2026-"},
    {"person_a": 9, "person_b": 10, "type": "共事", "context": "区委书记—人大主任", "overlap_org": "长春市九台区", "overlap_period": ""},
    {"person_a": 9, "person_b": 11, "type": "共事", "context": "区委书记—政协主席", "overlap_org": "长春市九台区", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "协助", "context": "党组成员协助副区长分管农业农村工作", "overlap_org": "九台区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "两位区委常委副区长", "overlap_org": "九台区政府", "overlap_period": "2026-"},
]

if __name__ == "__main__":
    run_build(
        slug="九台区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("Build complete!")
    print(f"  DB:  {DATABASE_DIR / '九台区_network.db'}")
    print(f"  GEXF: {GRAPH_DIR / '九台区_network.gexf'}")
