#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 阿克塞哈萨克族自治县 leadership network.

Data source: www.akesai.gov.cn (official government website)
Information currency: 2026-07 (current as of July 2026)
"""
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "阿克塞县"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: akesai_<pinyin_name>
persons = [
    # --- 县委领导班子 (Party Committee) ---
    {
        "id": 1, "name": "张桐", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共阿克塞哈萨克族自治县委员会",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 2, "name": "库美斯剑", "gender": "", "ethnicity": "哈萨克族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    # --- 县政府领导班子 (County Government) ---
    {
        "id": 3, "name": "杨国平", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 4, "name": "张国", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 5, "name": "尚帅", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 6, "name": "李春华", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 7, "name": "巴依哈孜", "gender": "", "ethnicity": "哈萨克族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 8, "name": "钟兴鹏", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 9, "name": "卢保健", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    {
        "id": 10, "name": "刘蓉", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100298/jgjj_xxgk.shtml",
    },
    # --- Additional government leaders from news reports ---
    {
        "id": 11, "name": "张鹏", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县领导",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100287/202503/1a8a388b5ef44f29824d011a45c90511.shtml",
    },
    {
        "id": 12, "name": "张健", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县领导",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100287/202503/1a8a388b5ef44f29824d011a45c90511.shtml",
    },
    {
        "id": 13, "name": "武海龙", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县领导",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100287/202503/1a8a388b5ef44f29824d011a45c90511.shtml",
    },
    {
        "id": 14, "name": "李珊珊", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县领导",
        "current_org": "阿克塞哈萨克族自治县人民政府",
        "source": "https://www.akesai.gov.cn/akshskz/c100287/202503/1a8a388b5ef44f29824d011a45c90511.shtml",
    },
    # --- 人大 & 政协 ---
    {
        "id": 15, "name": "塞力古", "gender": "", "ethnicity": "哈萨克族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "阿克塞哈萨克族自治县人大常委会",
        "source": "https://www.akesai.gov.cn/akshskz/c100287/202503/1a8a388b5ef44f29824d011a45c90511.shtml",
    },
    {
        "id": 16, "name": "包远泠", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议阿克塞哈萨克族自治县委员会",
        "source": "https://www.akesai.gov.cn/akshskz/c100287/202503/1a8a388b5ef44f29824d011a45c90511.shtml",
    },
    # --- Former leadership ---
    {
        "id": 17, "name": "陶涛", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共阿克塞哈萨克族自治县委员会",
        "source": "https://www.akesai.gov.cn/akshskz/c100287/202503/b095bdd681e744bfb760e55eff9c2dc5.shtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1, "name": "中共阿克塞哈萨克族自治县委员会",
        "type": "党委", "level": "县处级", "parent": "中共酒泉市委",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 2, "name": "阿克塞哈萨克族自治县人民政府",
        "type": "政府", "level": "县处级", "parent": "酒泉市人民政府",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 3, "name": "阿克塞哈萨克族自治县人大常委会",
        "type": "人大", "level": "县处级", "parent": "酒泉市人大常委会",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 4, "name": "中国人民政治协商会议阿克塞哈萨克族自治县委员会",
        "type": "政协", "level": "县处级", "parent": "政协酒泉市委员会",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 5, "name": "中国共产党阿克塞哈萨克族自治县纪律检查委员会",
        "type": "纪委", "level": "县处级", "parent": "中共酒泉市纪委",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 6, "name": "中共阿克塞哈萨克族自治县委组织部",
        "type": "党委部门", "level": "县处级", "parent": "中共阿克塞县委",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 7, "name": "中共阿克塞哈萨克族自治县委宣传部",
        "type": "党委部门", "level": "县处级", "parent": "中共阿克塞县委",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 8, "name": "中共阿克塞哈萨克族自治县委政法委",
        "type": "党委部门", "level": "县处级", "parent": "中共阿克塞县委",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
    {
        "id": 9, "name": "中共阿克塞哈萨克族自治县委统战部",
        "type": "党委部门", "level": "县处级", "parent": "中共阿克塞县委",
        "location": "甘肃省酒泉市阿克塞哈萨克族自治县",
    },
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 张桐
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "~2026", "end_date": "", "rank": "正县级", "note": "接替陶涛，具体上任时间未公开"},
    # 库美斯剑
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正县级", "note": "哈萨克族，主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 副县长
    {"person_id": 3, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "哈萨克族"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "女性"},
    # 其他县领导 (from news reports)
    {"person_id": 11, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "", "rank": "副县级", "note": "具体职务未确认"},
    {"person_id": 12, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "", "rank": "副县级", "note": "具体职务未确认"},
    {"person_id": 13, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "", "rank": "副县级", "note": "具体职务未确认"},
    {"person_id": 14, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "", "rank": "副县级", "note": "女性，具体职务未确认"},
    # 人大
    {"person_id": 15, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 政协
    {"person_id": 16, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 前任
    {"person_id": 17, "org_id": 1, "title": "县委书记", "start_date": "~2021", "end_date": "~2026", "rank": "正县级", "note": "被省委巡视组反馈巡视情况(2025.03)，后被张桐接替"},
]

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    # 县委书记—县长
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记—县长", "overlap_org": "阿克塞县四套班子", "overlap_period": "2026—"},
    # 县长—副县长（政府班子成员）
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "阿克塞县人民政府", "overlap_period": ""},
    # 前任—现任书记
    {"person_a": 17, "person_b": 1, "type": "前后任", "context": "前任县委书记→现任县委书记", "overlap_org": "中共阿克塞县委", "overlap_period": "~2025-2026交接"},
    # 人大列席政府会议
    {"person_a": 15, "person_b": 2, "type": "列席监督", "context": "人大常委会副主任列席县政府常务会议", "overlap_org": "阿克塞县四套班子", "overlap_period": "2025—"},
    # 政协列席政府会议
    {"person_a": 16, "person_b": 2, "type": "列席监督", "context": "政协副主席列席县政府常务会议", "overlap_org": "阿克塞县四套班子", "overlap_period": "2025—"},
]

# ── Run Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "阿克塞县_network.db",
        gexf_path=GRAPH_DIR / "阿克塞县_network.gexf",
        overwrite=True,
    )
    print("Done: 阿克塞县 network built.")
