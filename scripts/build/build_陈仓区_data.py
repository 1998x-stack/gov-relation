#!/usr/bin/env python3
"""
陈仓区领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件
"""
import sys
import os
import sqlite3  # noqa: used by gov_relation.schema
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))
os.chdir(str(REPO_ROOT))

from gov_relation.runner import run_build

# ===== 任务信息 =====
SLUG = "陈仓区"
TODAY = "2026-07-25"

# Person IDs to symbolic names for GEXF node labels
PERSON_NAMES = {
    1: "马霄",
    2: "马小锋",
    3: "裴振强",
    4: "苟晓明",
    5: "吴晶",
    6: "齐晓辉",
    7: "王晓妮",
    8: "高玉文",
}

persons = [
    {"id": 1, "name": "马霄", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "陈仓区委书记", "current_org": "中共宝鸡市陈仓区委员会", "source": "www.chencang.gov.cn - 区政协四届五次会议(2026-01-21)"},
    {"id": 2, "name": "马小锋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "陈仓区委副书记、区长", "current_org": "陈仓区人民政府", "source": "www.chencang.gov.cn - 区政协四届五次会议(2026-01-21)"},
    {"id": 3, "name": "裴振强", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "陈仓区人大常委会主任", "current_org": "陈仓区人大常委会", "source": "www.chencang.gov.cn - 区纪委六次全会(2026-02-11)"},
    {"id": 4, "name": "苟晓明", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "陈仓区政协主席", "current_org": "政协宝鸡市陈仓区委员会", "source": "www.chencang.gov.cn - 区政协四届五次会议(2026-01-21)"},
    {"id": 5, "name": "吴晶", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "陈仓区委常委、区纪委书记、区监委主任", "current_org": "中共宝鸡市陈仓区纪律检查委员会", "source": "www.chencang.gov.cn - 区纪委六次全会(2026-02-11)"},
    {"id": 6, "name": "齐晓辉", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "陈仓区副区长", "current_org": "陈仓区人民政府", "source": "www.chencang.gov.cn - 宝职院合作(2026-06-29)"},
    {"id": 7, "name": "王晓妮", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "陈仓区政协副主席", "current_org": "政协宝鸡市陈仓区委员会", "source": "www.chencang.gov.cn - 区政协四届五次会议(2026-01-21)"},
    {"id": 8, "name": "高玉文", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "", "current_post": "陈仓区政协副主席", "current_org": "政协宝鸡市陈仓区委员会", "source": "www.chencang.gov.cn - 区政协四届五次会议(2026-01-21)"},
]

organizations = [
    {"id": 1, "name": "中共宝鸡市陈仓区委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "陕西省宝鸡市陈仓区"},
    {"id": 2, "name": "陈仓区人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "陕西省宝鸡市陈仓区"},
    {"id": 3, "name": "陈仓区人大常委会", "type": "人大", "level": "县处级", "parent": "宝鸡市人大常委会", "location": "陕西省宝鸡市陈仓区"},
    {"id": 4, "name": "政协宝鸡市陈仓区委员会", "type": "政协", "level": "县处级", "parent": "政协宝鸡市委员会", "location": "陕西省宝鸡市陈仓区"},
    {"id": 5, "name": "中共宝鸡市陈仓区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市纪委监委", "location": "陕西省宝鸡市陈仓区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "陈仓区委书记", "start_date": "", "end_date": "present", "rank": "正县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "陈仓区区长", "start_date": "", "end_date": "present", "rank": "正县处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "陈仓区委副书记", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "陈仓区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "陈仓区政协主席", "start_date": "", "end_date": "present", "rank": "正县处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "陈仓区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "陈仓区委常委", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "陈仓区副区长", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "陈仓区政协副主席", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "陈仓区政协副主席", "start_date": "", "end_date": "present", "rank": "副县处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政协同", "context": "区委书记与区长搭档", "overlap_org": "中共宝鸡市陈仓区委员会/陈仓区人民政府", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "领导合作", "context": "区委书记与区人大常委会主任共同出席重要会议", "overlap_org": "陈仓区", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "领导合作", "context": "区委书记与区政协主席共同出席区政协会议并发表讲话", "overlap_org": "陈仓区", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与区纪委书记，在区纪委六次全会上马霄讲话、吴晶主持", "overlap_org": "中共宝鸡市陈仓区委员会", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "领导合作", "context": "区长与区人大常委会主任共同出席区级重要会议", "overlap_org": "陈仓区", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "领导合作", "context": "区长与区政协主席共同出席区政协会议", "overlap_org": "陈仓区", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与副区长，共同出席宝职院与陈仓医院合作揭牌仪式", "overlap_org": "陈仓区人民政府", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "领导合作", "context": "马小锋在区纪委六次全会上传达学习习近平总书记重要讲话精神", "overlap_org": "陈仓区", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 4, "type": "上下级", "context": "区政协副主席与区政协主席共同履职", "overlap_org": "政协宝鸡市陈仓区委员会", "overlap_period": "现任期间", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 4, "type": "上下级", "context": "区政协副主席与区政协主席共同履职", "overlap_org": "政协宝鸡市陈仓区委员会", "overlap_period": "现任期间", "confidence": "confirmed"},
]

if __name__ == "__main__":
    STAGING_DIR = Path(__file__).resolve().parent
    DB_PATH = STAGING_DIR / "陈仓区_network.db"
    GEXF_PATH = STAGING_DIR / "陈仓区_network.gexf"

    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print("=" * 60)

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

    print(f"\n  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人, 机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条, 关系: {len(relationships)} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")
