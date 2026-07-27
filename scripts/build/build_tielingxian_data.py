#!/usr/bin/env python3
"""Build SQLite DB and GEXF graph for 铁岭县 leadership network."""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "铁岭县"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: 10-19 party committee, 20-29 government, 30-39 other
persons = [
    # ── Party Committee (县委) ──
    {
        "id": 10,
        "name": "付尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共铁岭县委员会",
        "source": "https://www.tielingxian.gov.cn/tlx/xwzx/tlxxw/2026070708494779579/index.html",
    },
    {
        "id": 11,
        "name": "朱善植",
        "gender": "男",
        "ethnicity": "朝鲜族",
        "birth": "1985年8月",
        "birthplace": "待查",
        "education": "研究生学历，管理学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/xz/2022031922241534450/index.html",
    },
    {
        "id": 12,
        "name": "滕达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "待查",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2025030708244779386/index.html",
    },
    {
        "id": 13,
        "name": "钟鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "待查",
        "education": "硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2025022411482388742/index.html",
    },
    # ── Government (县政府, not party standing committee members) ──
    {
        "id": 20,
        "name": "李文涛",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铁岭铁南经济开发区管委会主任",
        "current_org": "铁岭铁南经济开发区管委会",
        "source": "https://www.tielingxian.gov.cn/tlx/zwgk/zfwj/xzfbgswj/2026042410063843433/index.html",
    },
    {
        "id": 21,
        "name": "张宏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "待查",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2026071314124848468/index.html",
    },
    {
        "id": 22,
        "name": "崔佳志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年4月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2023112810494963025/index.html",
    },
    {
        "id": 23,
        "name": "邓大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "待查",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2024092609324396509/index.html",
    },
    {
        "id": 24,
        "name": "李文罡",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1975年6月",
        "birthplace": "待查",
        "education": "大学学历，法学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2022031922241369056/index.html",
    },
    {
        "id": 25,
        "name": "刘军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "待查",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2023042708425811118/index.html",
    },
    {
        "id": 26,
        "name": "龙朕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "待查",
        "education": "研究生学历，硕士学位",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2022031922241382826/index.html",
    },
    {
        "id": 27,
        "name": "张睿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1995年11月",
        "birthplace": "待查",
        "education": "全日制研究生学历，管理学博士，农业资源与环境博士后",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职/锻炼）",
        "current_org": "铁岭县人民政府",
        "source": "https://www.tielingxian.gov.cn/tlx/xxgk/fdzdgknr/jgjj/xzfld/fxz/2025030308424083354/index.html",
    },
    # ── Other key officials ──
    {
        "id": 30,
        "name": "孙忠海",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原副县长（已离任）",
        "current_org": "待查",
        "source": "https://www.tielingxian.gov.cn/tlx/zwgk/zfwj/xzfbgswj/2026042410063843433/index.html",
    },
    {
        "id": 31,
        "name": "银洪阁",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "铁岭县人大常委会",
        "source": "https://www.tielingxian.gov.cn/tlx/xwzx/tlxxw/2026071309242227439/index.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
orgs = [
    {"id": 1, "name": "中共铁岭县委员会", "type": "党委", "level": "县级", "parent": "中共铁岭市委员会", "location": "铁岭市"},
    {"id": 2, "name": "铁岭县人民政府", "type": "政府", "level": "县级", "parent": "铁岭市人民政府", "location": "铁岭市"},
    {"id": 3, "name": "铁岭县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "铁岭市"},
    {"id": 4, "name": "铁岭铁南经济开发区管委会", "type": "开发区管委会", "level": "县级", "parent": "铁岭县人民政府", "location": "铁岭市"},
    {"id": 5, "name": "铁岭县公安局", "type": "政府组成部门", "level": "县级", "parent": "铁岭县人民政府", "location": "铁岭市"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 付尧
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
    # 朱善植
    {"person_id": 11, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县长、党组书记", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
    # 滕达
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "常务副县长、党组副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 钟鑫
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责国企国资改革、招商引资"},
    # 李文涛
    {"person_id": 20, "org_id": 4, "title": "管委会主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责工业、科技、民营经济"},
    # 张宏
    {"person_id": 21, "org_id": 2, "title": "副县长", "start_date": "2026年6月", "end_date": "", "rank": "副县级", "note": "负责住建、城管、商务、市场监管"},
    # 崔佳志
    {"person_id": 22, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责金融工作"},
    # 邓大伟
    {"person_id": 23, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责教育、自然资源、交通、文旅"},
    # 李文罡
    {"person_id": 24, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责公安、打私"},
    {"person_id": 24, "org_id": 5, "title": "局长、督察长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    # 刘军
    {"person_id": 25, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责生态环境、农业农村、林业、水利"},
    # 龙朕
    {"person_id": 26, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "负责卫健、民政、退役军人、医保"},
    # 张睿
    {"person_id": 27, "org_id": 2, "title": "副县长（挂职/锻炼）", "start_date": "", "end_date": "", "rank": "副县级", "note": "协助李文涛、刘军"},
    # 孙忠海
    {"person_id": 30, "org_id": 2, "title": "原副县长", "start_date": "", "end_date": "2026年6月", "rank": "副县级", "note": "原负责住建、商务、市场监管，已被张宏接替"},
    # 银洪阁
    {"person_id": 31, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 10, "person_b": 11, "type": "党政搭档", "context": "县委书记—县长搭档", "overlap_org": "中共铁岭县委员会", "overlap_period": ""},
    # 县委书记—常务副县长
    {"person_a": 10, "person_b": 12, "type": "上下级", "context": "县委书记—县委常委、常务副县长", "overlap_org": "中共铁岭县委员会", "overlap_period": ""},
    # 县长—常务副县长
    {"person_a": 11, "person_b": 12, "type": "上下级", "context": "县长—常务副县长（AB角互补）", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    # 县长—副县长
    {"person_a": 11, "person_b": 13, "type": "上下级", "context": "县长—县委常委、副县长", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 21, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 22, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 23, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 24, "type": "上下级", "context": "县长—副县长、公安局长", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 25, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 26, "type": "上下级", "context": "县长—副县长", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 27, "type": "上下级", "context": "县长—副县长（挂职）", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 20, "type": "上下级", "context": "县长—开发区管委会主任", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    # 县委常委之间
    {"person_a": 12, "person_b": 13, "type": "同级", "context": "县委常委（常务副县长—副县长）", "overlap_org": "中共铁岭县委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 13, "type": "上下级", "context": "县委书记—县委常委、副县长", "overlap_org": "中共铁岭县委员会", "overlap_period": ""},
    # AB角互补关系
    {"person_a": 12, "person_b": 20, "type": "AB角", "context": "滕达—李文涛 AB角互补", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 21, "person_b": 26, "type": "AB角", "context": "张宏—龙朕 AB角互补", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 27, "type": "AB角", "context": "钟鑫—张睿 AB角互补", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 22, "person_b": 25, "type": "AB角", "context": "崔佳志—刘军 AB角互补", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    {"person_a": 23, "person_b": 24, "type": "AB角", "context": "邓大伟—李文罡 AB角互补", "overlap_org": "铁岭县人民政府", "overlap_period": ""},
    # 前后任
    {"person_a": 30, "person_b": 21, "type": "前后任", "context": "孙忠海（原）→ 张宏（现）接替住建、商务、市场监管分工", "overlap_org": "铁岭县人民政府", "overlap_period": "2026年4月-6月"},
]

if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=orgs,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "铁岭县_network.db",
        gexf_path=GRAPH_DIR / "铁岭县_network.gexf",
        overwrite=True,
    )
    print("Done: 铁岭县 network built successfully!")
