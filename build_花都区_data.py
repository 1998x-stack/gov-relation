#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 花都区 (Huadu District) leadership network.

Data sources:
 - huadu.gov.cn/xxgk/ldzc/qzfld/ (official government leadership page)
 - huadu.gov.cn news articles (2026-07-22, 2026-07-17, 2026-07-10)
 - zh.wikipedia.org/wiki/花都区

Information currency: 2026-07-22 (current as of July 2026)
"""
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "花都区"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: huadu_<pinyin_name>
persons = [
    # ═══ Top Leaders (confirmed from official news 2026-07-22) ═══
    {
        "id": 1, "name": "邢翔", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共广州市花都区委员会",
        "source": "https://www.huadu.gov.cn/hdzx/hdxw/content/post_10912358.html",
    },
    {
        "id": 2, "name": "李晓东", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年11月", "birthplace": "", "education": "在职研究生学历，工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "广州市花都区人民政府",
        "source": "https://www.huadu.gov.cn/xxgk/ldzc/qzfld/lxd/index.html",
    },
    # ═══ 区人大常委会、区政协 ═══
    {
        "id": 3, "name": "李波", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "广州市花都区人大常委会",
        "source": "https://www.huadu.gov.cn/hdzx/hdxw/content/post_10912358.html",
    },
    {
        "id": 4, "name": "罗干政", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议广州市花都区委员会",
        "source": "https://www.huadu.gov.cn/hdzx/hdxw/content/post_10912358.html",
    },
    # ═══ 区委副书记 ═══
    {
        "id": 5, "name": "郑重民", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共广州市花都区委员会",
        "source": "https://www.huadu.gov.cn/hdzx/hdxw/content/post_10905519.html",
    },
    # ═══ 区委组织部 ═══
    {
        "id": 6, "name": "王智丰", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共广州市花都区委组织部",
        "source": "https://www.huadu.gov.cn/hdzx/hdxw/content/post_10905519.html",
    },
    # ═══ 区政府副区长 (from official leadership page) ═══
    {
        "id": 7, "name": "蔡启良", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年2月", "birthplace": "", "education": "本科学历，法学学士",
        "party_join": "民革成员", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市花都区人民政府",
        "source": "https://www.huadu.gov.cn/xxgk/ldzc/qzfld/cql/index.html",
    },
    {
        "id": 8, "name": "麦韶明", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年12月", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市花都区人民政府",
        "source": "https://www.huadu.gov.cn/xxgk/ldzc/qzfld/msm/index.html",
    },
    {
        "id": 9, "name": "胡标发", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年7月", "birthplace": "", "education": "大学学历，工程硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市花都区人民政府",
        "source": "https://www.huadu.gov.cn/xxgk/ldzc/qzfld/hbf/index.html",
    },
    {
        "id": 10, "name": "徐容雅", "gender": "女", "ethnicity": "汉族",
        "birth": "1980年6月", "birthplace": "", "education": "研究生学历，法学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副区长",
        "current_org": "广州市花都区人民政府",
        "source": "https://www.huadu.gov.cn/xxgk/ldzc/qzfld/xry/index.html",
    },
    {
        "id": 11, "name": "辜少辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1969年11月", "birthplace": "", "education": "在职大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "广州市花都区人民政府",
        "source": "https://www.huadu.gov.cn/xxgk/ldzc/qzfld/gsh/index.html",
    },
    {
        "id": 12, "name": "杨斐", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年9月", "birthplace": "", "education": "研究生学历，工学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "广州市花都区人民政府",
        "source": "https://www.huadu.gov.cn/xxgk/ldzc/qzfld/yf/index.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1, "name": "中共广州市花都区委员会",
        "type": "党委", "level": "副厅级", "parent": "中共广州市委",
        "location": "广东省广州市花都区",
    },
    {
        "id": 2, "name": "广州市花都区人民政府",
        "type": "政府", "level": "副厅级", "parent": "广州市人民政府",
        "location": "广东省广州市花都区",
    },
    {
        "id": 3, "name": "广州市花都区人大常委会",
        "type": "人大", "level": "副厅级", "parent": "广州市人大常委会",
        "location": "广东省广州市花都区",
    },
    {
        "id": 4, "name": "中国人民政治协商会议广州市花都区委员会",
        "type": "政协", "level": "副厅级", "parent": "政协广州市委员会",
        "location": "广东省广州市花都区",
    },
    {
        "id": 5, "name": "中共广州市花都区委组织部",
        "type": "党委部门", "level": "县处级", "parent": "中共广州市花都区委员会",
        "location": "广东省广州市花都区",
    },
    {
        "id": 6, "name": "广州市公安局花都区分局",
        "type": "政府", "level": "县处级", "parent": "广州市花都区人民政府",
        "location": "广东省广州市花都区",
    },
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 邢翔
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "已确认在任（2026年7月）"},
    # 李晓东
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李波
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 罗干政
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 郑重民
    {"person_id": 5, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王智丰
    {"person_id": 6, "org_id": 5, "title": "区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 蔡启良
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民革成员，负责工业/信息/人社/商贸/科技/金融/物流/侨务"},
    # 麦韶明
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "区政府党组成员，负责住建/城市更新/水务/信访/生态环境"},
    # 胡标发
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "区政府党组成员，负责卫健/农业农村/乡村振兴/退役军人/市场监管"},
    # 徐容雅
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "区政府党组成员，负责民政/城管/文旅体育/妇女儿童"},
    # 辜少辉
    {"person_id": 11, "org_id": 2, "title": "副区长、区公安分局局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "区政府党组成员，负责公安/禁毒/司法/武装"},
    {"person_id": 11, "org_id": 6, "title": "区公安分局党委书记、局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 杨斐
    {"person_id": 12, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "区政府党组成员，挂职，负责发改/教育/交通/政务数据"},
]

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    # 区委书记—区长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长", "overlap_org": "花都区四套班子", "overlap_period": "2026—"},
    # 区委书记—人大主任
    {"person_a": 1, "person_b": 3, "type": "党政搭档", "context": "区委书记—人大常委会主任", "overlap_org": "花都区四套班子", "overlap_period": "2026—"},
    # 区委书记—政协主席
    {"person_a": 1, "person_b": 4, "type": "党政搭档", "context": "区委书记—政协主席", "overlap_org": "花都区四套班子", "overlap_period": "2026—"},
    # 区委书记—区委副书记
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "中共花都区委", "overlap_period": "2026—"},
    # 区长—区委副书记（同一人已体现在人员结构）
    # 区长—副区长（政府班子）
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "花都区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "花都区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长—副区长", "overlap_org": "花都区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长—副区长", "overlap_org": "花都区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长—副区长", "overlap_org": "花都区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长—副区长（挂职）", "overlap_org": "花都区人民政府", "overlap_period": ""},
    # 区委组织部部长—区委书记
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—组织部部长", "overlap_org": "中共花都区委", "overlap_period": "2026—"},
]

# ── Run Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "花都区_network.db",
        gexf_path=GRAPH_DIR / "花都区_network.gexf",
        overwrite=True,
    )
    print("Done: 花都区 network built.")
