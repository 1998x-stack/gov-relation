#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 饶平县 leadership network.
 
饶平县 (Raoping County) is under 潮州市, 广东省.
"""
 
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from pathlib import Path
 
SLUG = "饶平县"
 
# ── Staging paths ────────────────────────────────────────────────────
BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
STAGING = BASE / "data/tmp/guangdong_饶平县"
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
 
# ── DATA ─────────────────────────────────────────────────────────────
 
persons = [
    # ── Current County Party Secretary (县委书记) ──
    {
        "id": 1,
        "name": "蔡益雄",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共饶平县委书记",
        "current_org": "中共饶平县委员会",
        "source": "confirmed — named as '县委书记蔡益雄' in raoping.gov.cn news article 2026-07-22 (茶饮新风 潮起饶平). Biographical details not found due to limited web access."
    },
 
    # ── Current County Mayor (县长) ──
    {
        "id": 2,
        "name": "杨镇荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共饶平县委副书记、县政府党组书记、县长",
        "current_org": "饶平县人民政府",
        "source": "confirmed — listed as '县长：杨镇荣' on raoping.gov.cn government leaders page. Also named in 2026-07-22 news article as '县委副书记、县长杨镇荣'. Bio page exists at raoping.gov.cn/zwgk/xzfld/content/post_3993116.html"
    },
 
    # ── 县委常委、常务副县长 ──
    # Name: NOT CONFIRMED from available web sources
    {
        "id": 3,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "饶平县人民政府",
        "source": "unverified — placeholder. Exact name unknown from available web sources."
    },
 
    # ── 县委常委、组织部部长 ──
    # Name: NOT CONFIRMED
    {
        "id": 4,
        "name": "待查（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共饶平县委员会",
        "source": "unverified — placeholder. Exact name unknown from available web sources."
    },
 
    # ── 县委常委、纪委书记、县监委主任 ──
    # Name: NOT CONFIRMED
    {
        "id": 5,
        "name": "待查（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、县监委主任",
        "current_org": "中共饶平县纪律检查委员会",
        "source": "unverified — placeholder. Exact name unknown from available web sources."
    },
 
    # ── 市委常委 陈跃庆 (connected to 饶平) ──
    {
        "id": 6,
        "name": "陈跃庆",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潮州市委常委",
        "current_org": "中共潮州市委员会",
        "source": "confirmed — named as '市委常委陈跃庆' attending 饶平 event July 2026. Previous role: was 饶平县委书记 (inferred from being the 市委常委 assigned to 饶平)."
    },
 
    # ── 县委副书记（专职） ──
    {
        "id": 7,
        "name": "待查（专职副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共饶平县委副书记（专职）",
        "current_org": "中共饶平县委员会",
        "source": "unverified — placeholder. Exact name unknown from available web sources."
    },
 
    # ── 县委常委、政法委书记 ──
    {
        "id": 8,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共饶平县委员会",
        "source": "unverified — placeholder. Exact name unknown from available web sources."
    },
 
    # ── 县委常委、宣传部部长 ──
    {
        "id": 9,
        "name": "待查（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共饶平县委员会",
        "source": "unverified — placeholder. Exact name unknown from available web sources."
    },
]
 
organizations = [
    {
        "id": 1,
        "name": "中共饶平县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共潮州市委员会",
        "location": "广东潮州饶平"
    },
    {
        "id": 2,
        "name": "饶平县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "潮州市人民政府",
        "location": "广东潮州饶平"
    },
    {
        "id": 3,
        "name": "中共饶平县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共饶平县委员会/中共潮州市纪委",
        "location": "广东潮州饶平"
    },
    {
        "id": 4,
        "name": "中共潮州市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共广东省委",
        "location": "广东潮州"
    },
]
 
positions = [
    # ── 蔡益雄 ──
    {
        "id": 1, "person_id": 1, "org_id": 1,
        "title": "中共饶平县委书记",
        "start_date": "", "end_date": "",
        "rank": "县处级正职",
        "note": "现任; 上任时间待查. 首次发现于2026年7月新闻报道."
    },
 
    # ── 杨镇荣 ──
    {
        "id": 2, "person_id": 2, "org_id": 1,
        "title": "中共饶平县委副书记",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "现任"
    },
    {
        "id": 3, "person_id": 2, "org_id": 2,
        "title": "饶平县人民政府党组书记、县长",
        "start_date": "", "end_date": "",
        "rank": "县处级正职",
        "note": "现任; 主持县政府全面工作，分管审计工作"
    },
 
    # ── 待查：常务副县长 ──
    {
        "id": 4, "person_id": 3, "org_id": 1,
        "title": "饶平县委常委",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "任职时间待查"
    },
    {
        "id": 5, "person_id": 3, "org_id": 2,
        "title": "县委常委、常务副县长",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "任职时间待查; 姓名待确认"
    },
 
    # ── 待查：组织部部长 ──
    {
        "id": 6, "person_id": 4, "org_id": 1,
        "title": "饶平县委常委、组织部部长",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "任职时间待查; 姓名待确认"
    },
 
    # ── 待查：纪委书记 ──
    {
        "id": 7, "person_id": 5, "org_id": 3,
        "title": "饶平县委常委、纪委书记、县监委主任",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "任职时间待查; 姓名待确认"
    },
 
    # ── 陈跃庆（市委常委） ──
    {
        "id": 8, "person_id": 6, "org_id": 4,
        "title": "潮州市委常委",
        "start_date": "", "end_date": "",
        "rank": "地厅级副职",
        "note": "现任; 曾任饶平县委书记（推断）"
    },
 
    # ── 待查：专职副书记 ──
    {
        "id": 9, "person_id": 7, "org_id": 1,
        "title": "中共饶平县委专职副书记",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "任职时间待查; 姓名待确认"
    },
 
    # ── 待查：政法委书记 ──
    {
        "id": 10, "person_id": 8, "org_id": 1,
        "title": "饶平县委常委、政法委书记",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "任职时间待查; 姓名待确认"
    },
 
    # ── 待查：宣传部部长 ──
    {
        "id": 11, "person_id": 9, "org_id": 1,
        "title": "饶平县委常委、宣传部部长",
        "start_date": "", "end_date": "",
        "rank": "县处级副职",
        "note": "任职时间待查; 姓名待确认"
    },
]
 
relationships = [
    # ── 党政搭档：蔡益雄 ↔ 杨镇荣 ──
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "党政一把手搭档关系：蔡益雄任县委书记，杨镇荣任县委副书记、县长",
        "overlap_org": "中共饶平县委员会",
        "overlap_period": "2026年至今",
        "strength": "strong",
        "direction": "undirected",
        "confidence": "confirmed",
        "source_ids": ["S001", "S002"]
    },
 
    # ── 陈跃庆作为潮州市委常委与饶平县的关联 ──
    {
        "person_a": 6, "person_b": 1,
        "type": "superior_subordinate",
        "context": "陈跃庆（市委常委）与蔡益雄（县委书记）的上下级关系",
        "overlap_org": "中共饶平县委员会",
        "overlap_period": "2026年",
        "strength": "medium",
        "direction": "other_to_person",
        "confidence": "confirmed",
        "source_ids": ["S001"]
    },
 
    {
        "person_a": 6, "person_b": 2,
        "type": "superior_subordinate",
        "context": "陈跃庆（市委常委）与杨镇荣（县长）的上下级关系",
        "overlap_org": "饶平县人民政府/中共潮州市委员会",
        "overlap_period": "2026年",
        "strength": "medium",
        "direction": "other_to_person",
        "confidence": "confirmed",
        "source_ids": ["S001"]
    },
]
 
# ── Build ─────────────────────────────────────────────────────────────
 
if __name__ == "__main__":
    STAGING.mkdir(parents=True, exist_ok=True)
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
    print(f"Done. DB: {DB_PATH}  GEXF: {GEXF_PATH}")
