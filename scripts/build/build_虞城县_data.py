#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 虞城县 (Yucheng County), 商丘市, 河南省.

Investigation date: 2026-08-06
Task ID: henan_虞城县
Level: 县
Targets: 县委书记 & 县长

Research sources (confirmed):
  - 河南县域经济网 sq.henance.com (转载虞城县融媒体中心):
    * 2026-01-05 十三届县委常委会第183次(扩大) (何玉东主持; 蒋验军、班春丽; 王计富、王奕朝、卓红兵) (https://sq.henance.com/show-61831.html)
    * 2026-02-26 十三届县委常委会第192次(扩大) (https://sq.henance.com/show-62429.html)
    * 2026-03-29 政绩观学习教育读书班 (https://sq.henance.com/show-62743.html)
    * 2026-04-09 十三届县委第199次常委会 (何玉东; 人大主任卓红兵) (https://sq.henance.com/show-62912.html)
    * 2026-05-09 县委书记吴杰调研政绩观学习教育 (https://sq.henance.com/show-63273.html)
    * 2026-05-26 县委书记吴杰调研食品安全 (https://sq.henance.com/show-63450.html)
    * 2026-05-27 县委书记吴杰调研安置区建设 (https://sq.henance.com/show-63480.html)
    * 2026-06-16 中共虞城县第十四次代表大会预备会议 (主席团: 吴杰、蒋验军、张晓辉等) (https://sq.henance.com/show-63725.html)
    * 2026-06-22 县委书记吴杰、县长蒋验军调研重点项目 (https://c.m.163.com/news/a/L21VVUMB05568W0A.html)
    * 2026-07-13 县政府第78次常务会议 (https://sq.henance.com/show-63959.html)
    * 2026-07-28 县领导"八一"慰问 (县委书记吴杰、县长蒋验军) (https://sq.henance.com/show-64090.html)
  - 商丘纪检监察网 www.sqlzw.gov.cn (虞城县纪委监委 领导机构: 书记/监委主任张晓辉) (https://www.sqlzw.gov.cn/yucheng/)
  - 河南省委组织部/新华网/人民网/大河网 2026-04-20 (领导干部任职前公示): "吴杰,1976-10,现任柘城县委副书记、县长,拟任县(市、区)委书记" (http://renshi.people.com.cn/n1/2026/0420/c139617-40704625.html)
  - 2023-05-18 中原新闻网: 何玉东任中共虞城县委书记 (https://www.zysbs.cn/html/zhoubian/sq/2023_05/18/82197600.html)
  - 2023-11-20 中原新闻网 公示 (蒋验军,1985-08, 研究生法学硕士, 现任虞城县委常、闻集镇党委书记, 拟任县长候选人) (https://www.zysbs.cn/.../82210829.html)
  - 2023-03-06 大河网 公示 (班春丽,1970-07,女,中专,现任虞城县委副书记/三级调研员, 拟任县长候选人) (https://city.dahe.cn/2023/03-06/1198550.html)
  - 2022-05 大河网 商丘县市区换届名单 (孙虎当选虞城县县长; 张晓辉监委主任; 王奕朝县政协主席) (https://5g.dahe.cn/news/202205011013555)
  - 中国县域 虞城县政府领导分工 (张伟常务副县长; 赵来霞宣传部长/副县长; 陈富磊、吴振兴、宋占珂、刘新学; 申法志/胡彦强挂职) (http://www.zgcounty.com/news/37239.html)
  - 虞城县2024/2025政府工作报告 (县长蒋验军) (http://www.zgcounty.com/news/55333.html)
  - 网易 商丘各(区)县现任书记汇总 (何玉东 梁园区人 1968-01 履历) (https://www.163.com/dy/article/I88AQDO505450VMH.html)
  - 河南省纪委监委/商丘市纪委监委 2025-07-11 虞城县原一级调研员逯德标接受审查调查; 2026-02被开除党籍移送司法机关 (http://www.nydi.gov.cn/sitesources/sqlzw/page_pc/gzdt/jdpg/article8c2c8b4247fa42d2b940034793513aa9.html)

Confidence notes:
  - 吴杰: confirmed 虞城县委书记 (2026-05起; 任前公示2026-04-20; 2026-06/07官方文章明确标注)
  - 蒋验军: confirmed 虞城县长 (2024-03当选, 2026年在任)
  - 何玉东: 2023-05~2026-04任虞城县委书记; 兼商丘市政协副主席; 2026年卸任后职务待查
  - 王计富/卓红兵: 人大主任交接 (2026), 卓红兵为人县人大常委会党组书记/主任
  - 逯德标(原一级调研员/常务副县长) 2025-07被查, 2026-02双开移送司法 —— 重大负向信号
  - 部分人物出生/学历/完整履历未完全公开, 标为 unverified/plausible
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "虞城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# ── Persons ────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1, "name": "吴杰", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-10", "birthplace": "河南省商丘市夏邑县",
        "education": "省委党校大学", "party_join": "", "work_start": "",
        "current_post": "县委书记", "current_org": "中共虞城县委员会",
        "source": "Confirmed 虞城县委书记 (2026-05起). 2026-04-20任前公示 '现任柘城县委副书记、县长,拟任县(市、区)委书记'. 曾任宁陵县委常/县委办主任、柘城县委常/常务副县长、柘城县委副书记/县长(2025-01当选). 2026-06虞城县第十四次党代会主席团首位."
    },
    {
        "id": 2, "name": "蒋验军", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-08", "birthplace": "",
        "education": "研究生、法学硕士", "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长", "current_org": "虞城县人民政府",
        "source": "Confirmed: 2023-11-20任前公示'虞城县委常、闻集镇党委书记,拟任县(市、区)长候选人,1985-08,研究生法学硕士'; 2023-12代县长; 2024-03-29县十六届人大四次会议当选县长; 2026年在任."
    },
    {
        "id": 3, "name": "何玉东", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-01", "birthplace": "河南省商丘市梁园区",
        "education": "大学(党校)", "party_join": "", "work_start": "",
        "current_post": "商丘市政协副主席（原虞城县委书记）", "current_org": "商丘市政协",
        "source": "Confirmed: 2023-05-17任虞城县委书记; 任内兼商丘市政协副主席; 曾任梁园区乡镇党委书记、梁园区副区长、商丘市工信局副局长(2021-08)、商丘市乡村振兴局党组书记/主任(2022-08). 2026年卸任虞城书记(吴杰接), 现任职务待查."
    },
    {
        "id": 4, "name": "班春丽", "gender": "女", "ethnicity": "汉族",
        "birth": "1970-07", "birthplace": "",
        "education": "中专", "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记", "current_org": "中共虞城县委员会",
        "source": "Confirmed via 2023-03-06任前公示'1970-07生,女,中专,现任虞城县委副书记/三级调研员,拟任县长候选人'; 后仍任县委副书记. 2016-2022曾任副县长、常务副县长."
    },
    {
        "id": 5, "name": "孙虎", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "（原虞城县县长）", "current_org": "",
        "source": "Confirmed: 2022-04-26十六届人大一次会议当选虞城县县长; 2021-12已以县长身份活动(人民日报中国品牌论坛). 2023-11蒋验军接任代县长, 孙虎卸任, 去向未确认."
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共虞城县委员会", "type": "党委", "level": "县处级", "parent": "中共商丘市委", "location": "虞城县"},
    {"id": 2, "name": "虞城县人民政府", "type": "政府", "level": "县处级", "parent": "商丘市人民政府", "location": "虞城县"},
    {"id": 3, "name": "虞城县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "商丘市人大常委会", "location": "虞城县"},
    {"id": 4, "name": "中国人民政治协商会议虞城县委员会", "type": "政协", "level": "县处级", "parent": "商丘市政协", "location": "虞城县"},
    {"id": 5, "name": "虞城县纪律检查委员会、监察委员会", "type": "纪委", "level": "县处级", "parent": "商丘市纪委监委", "location": "虞城县"},
    {"id": 6, "name": "商丘市人大常委会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "商丘市"},
    {"id": 7, "name": "中共商丘市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "商丘市"},
    {"id": 8, "name": "商丘市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "商丘市"},
    {"id": 9, "name": "中共柘城县委", "type": "党委", "level": "县处级", "parent": "中共商丘市委", "location": "柘城县"},
    {"id": 10, "name": "柘城县人民政府", "type": "政府", "level": "县处级", "parent": "商丘市人民政府", "location": "柘城县"},
    {"id": 11, "name": "商丘市政协", "type": "政协", "level": "地级市", "parent": "河南省政协", "location": "商丘市"},
    {"id": 12, "name": "中共宁陵县委", "type": "党委", "level": "县处级", "parent": "中共商丘市委", "location": "宁陵县"},
    {"id": 13, "name": "中共梁园区委", "type": "党委", "level": "副厅级", "parent": "中共商丘市委", "location": "商丘市梁园区"},
    {"id": 14, "name": "商丘市工业和信息化局", "type": "政府机关", "level": "正处级", "parent": "商丘市人民政府", "location": "商丘市"},
    {"id": 15, "name": "商丘市乡村振兴局", "type": "政府机关", "level": "正处级", "parent": "商丘市人民政府", "location": "商丘市"},
    {"id": 16, "name": "虞城县闻集镇党委、政府", "type": "乡镇/街道", "level": "乡科级", "parent": "虞城县人民政府", "location": "虞城县闻集镇"},
]

# ── Positions (person → org with title) ───────────────────────────────
positions = [
    # 吴杰 (id=1)
    {"person_id": 1, "org_id": 12, "title": "宁陵县委常委、县委办公室主任", "start_date": "unknown", "end_date": "unknown", "rank": "县处级副职", "note": "曾任"},
    {"person_id": 1, "org_id": 9, "title": "柘城县委常委、常务副县长", "start_date": "unknown", "end_date": "2023-01", "rank": "县处级副职", "note": "曾任"},
    {"person_id": 1, "org_id": 9, "title": "柘城县委副书记", "start_date": "2023", "end_date": "2025-01", "rank": "县处级副职", "note": "任柘城县委副书记"},
    {"person_id": 1, "org_id": 10, "title": "柘城县委副书记、县长", "start_date": "2025-01-25", "end_date": "2026-04", "rank": "县处级正职", "note": "2025-01-25柘城县十六届人大五次会议当选县长"},
    {"person_id": 1, "org_id": 1, "title": "虞城县委书记", "start_date": "2026-05", "end_date": "present", "rank": "县处级正职", "note": "2026-04-20任前公示; 2026-05起以县委书记活动"},
    # 蒋验军 (id=2)
    {"person_id": 2, "org_id": 1, "title": "虞城县委常委", "start_date": "unknown", "end_date": "2023-11", "rank": "县处级副职", "note": "兼闻集镇党委书记"},
    {"person_id": 2, "org_id": 16, "title": "闻集镇党委书记", "start_date": "unknown", "end_date": "2023-11", "rank": "乡科级正职", "note": "兼"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "2023-12", "end_date": "2024-03", "rank": "县处级正职", "note": "2023-12任代县长"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2024-03-29", "end_date": "present", "rank": "县处级正职", "note": "2024-03-29县十六届人大四次会议当选"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2023-12", "end_date": "present", "rank": "县处级副职", "note": "县长兼任县委副书记"},
    # 何玉东 (id=3)
    {"person_id": 3, "org_id": 13, "title": "梁园区乡镇党委书记、副区长", "start_date": "unknown", "end_date": "2021-08", "rank": "区级副职", "note": "基层乡镇党委书记; 梁园区副区长、三级调研员"},
    {"person_id": 3, "org_id": 14, "title": "商丘市工信局副局长", "start_date": "2021-08", "end_date": "2022-08", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 15, "title": "商丘市乡村振兴局党组书记、局长", "start_date": "2022-08", "end_date": "2023-05", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "虞城县委书记", "start_date": "2023-05-17", "end_date": "2026-04", "rank": "县处级正职", "note": "2023-05-17任职"},
    {"person_id": 3, "org_id": 11, "title": "商丘市政协副主席", "start_date": "unknown", "end_date": "present", "rank": "厅级", "note": "任虞城书记期间兼任"},
    # 班春丽 (id=4)
    {"person_id": 4, "org_id": 2, "title": "虞城县副县长", "start_date": "2016", "end_date": "2020", "rank": "县处级副职", "note": "2022选举名单列副县长"},
    {"person_id": 4, "org_id": 2, "title": "虞城县委常委、常务副县长", "start_date": "2020", "end_date": "2022-03", "rank": "县处级副职", "note": "2022-03县长议事会为常务副县长"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "2022", "end_date": "present", "rank": "县处级副职", "note": "2023-03拟任县长候选人未获任,后仍任副书记"},
    # 孙虎 (id=5)
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start_date": "2021", "end_date": "2023-11", "rank": "县处级副职", "note": "县长兼任"},
    {"person_id": 5, "org_id": 2, "title": "县长", "start_date": "2022-04-26", "end_date": "2023-11", "rank": "县处级正职", "note": "2022-04-26当选; 2021-12已为县长"},
]

# ── Relationships ─────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "吴杰（县委书记）与蒋验军（县委副书记、县长）为虞城全县党政正职搭档，共同主持县委县政府工作（2026-06 重点项目调研、2026-07 八一慰问等多次同场）。",
     "overlap_org": "虞城县", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "何玉东 2026-04 卸任虞城县委书记，吴杰接任（2026-05），由商丘市委主导任免交接。",
     "overlap_org": "中共虞城县委员会", "overlap_period": "2026-05"},
    {"person_a": 3, "person_b": 2, "type": "overlap",
     "context": "何玉东任虞城县委书记（2023-05~2026-04）期间，与县委副书记、县长蒋验军（2024起）为党政正职搭档。",
     "overlap_org": "虞城县", "overlap_period": "2024-2026"},
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor",
     "context": "孙飞 2021~2023任虞城县长，蒋验军 2023-11 公示候任代县长接任。",
     "overlap_org": "虞城县人民政府", "overlap_period": "2023-11"},
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor",
     "context": "班春丽 2023-03 公示拟任县长候选人未获任；蒋验军 2023-11 获任代县长，同一县长职务交替。",
     "overlap_org": "虞城县", "overlap_period": "2023"},
    {"person_a": 1, "person_b": 3, "type": "cross_county",
     "context": "吴杰（宁陵→柘城→虞城）与何玉东（梁园区→市直→虞城）同属商丘市委辖下跨县/市直多岗位轮换的县处级正职领导线路。",
     "overlap_org": "中共商丘市委", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "same_org",
     "context": "蒋验军（县长）与班春丽（县委副书记）同届虞城县党政班子共事。",
     "overlap_org": "虞城县", "overlap_period": "2023-至今"},
]

# ── Person JSON Data ──────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1, "name": "吴杰", "job": "县委书记",
        "data": {
            "schema_version": "1.0", "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "商丘市", "region": "虞城县", "job": "县委书记", "task_id": "henan_虞城县", "time_focus": "2021-2026"},
            "identity": {
                "name": "吴杰", "person_id": "yucheng_wu_jie", "aliases": [], "gender": "男", "ethnicity": "汉族",
                "birth": "1976-10", "birthplace": "河南省商丘市夏邑县", "native_place": "河南夏邑",
                "education": [{"period": "", "institution": "省委党校", "major": "", "degree": "大学", "study_type": "party_school", "source_ids": ["S001"]}],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "吴杰_197610", "name_birthplace": "吴杰_河南夏邑", "official_profile_url": "https://baike.baidu.com/item/吴杰"}
            },
            "current_status": {"current_post": "县委书记", "current_org": "中共虞城县委员会", "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
            "career_timeline": [
                {"start": "unknown", "end": "unknown", "org": "中共宁陵县委", "title": "县委常委、县委办公室主任", "level": "县处级副职", "location": "宁陵县", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "曾任宁陵县委常、县委办公室主任（百科）", "confidence": "plausible", "source_ids": ["S004"]},
                {"start": "unknown", "end": "2023-01", "org": "中共柘城县委", "title": "县委常委、常务副县长", "level": "县处级副职", "location": "柘城县", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "柘城县委常委、常务副县长", "confidence": "plausible", "source_ids": ["S004"]},
                {"start": "2023", "end": "2025-01", "org": "中共柘城县委", "title": "县委副书记", "level": "县处级副职", "location": "柘城县", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "任柘城县委副书记", "confidence": "plausible", "source_ids": ["S004"]},
                {"start": "2025-01-25", "end": "2026-04", "org": "柘城县人民政府", "title": "县长", "level": "县处级正职", "location": "柘城县", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "2025-01-25柘城县十六届人大五次会议当选县长", "confidence": "confirmed", "source_ids": ["S004", "S001"]},
                {"start": "2026-05", "end": "present", "org": "中共虞城县委员会", "title": "县委书记", "level": "县处级正职", "location": "虞城县", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2026-04-20任前公示; 2026-05起任县委书记", "confidence": "confirmed", "source_ids": ["S001", "S002"]}
            ],
            "organizations": [
                {"org": "中共宁陵县委", "role": "县委常/县委办主任", "period": "unknown"},
                {"org": "柘城县人民政府", "role": "县长", "period": "2025-2026"},
                {"org": "中共虞城县委员会", "role": "县委书记", "period": "2026-至今"}
            ],
            "relationships": [
                {"person": "蒋验军", "person_id": "yucheng_jiang_yanjun", "relationship_type": "overlap", "strength": "strong", "evidence": "吴杰（书记）与蒋验军（县长）为全县党政正职搭档，多次同场出席会议调研。", "overlap_org": "虞城县", "overlap_period": "2026-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
                {"person": "何玉东", "person_id": "yucheng_he_yudong", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "何玉东2026-04卸任虞城书记，吴杰接任（前后任交接）。", "overlap_org": "中共虞城县委员会", "overlap_period": "2026-05", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {"period": "2026-05-25", "domain": "public_security", "achievement_or_event": "带队食品安全专题调研（商超/学校/食品生产企业/餐饮），强调'四个最严'。", "role_in_event": "带队调研", "location": "虞城县", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-06-22", "domain": "economic_development", "achievement_or_event": "深入重点企业重点项目调研（食品/家居/工业），督进度解难题。", "role_in_event": "带队调研", "location": "虞城县", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2026-05-27", "domain": "urban_construction", "achievement_or_event": "安置区建设调研，强调以市场化盘活存量资源、保障回迁群众安居。", "role_in_event": "带队调研", "location": "虞城县", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "professional_profile": {
                "primary_specializations": ["县域经济", "工业/项目", "民生/食品安全"], "secondary_specializations": ["安全生产", "政绩观学习教育"],
                "career_pattern": "cross_county_rotation", "systems_experience": ["party", "government"],
                "geographic_pattern": ["河南省商丘市宁陵县/柘城县/虞城县"],
                "promotion_velocity": {"summary": "2025-01任柘城县长，2026-05升任虞城县委书记，约一年多从县长到书记，组织常规晋升。", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "频繁深入乡镇、企业、学校、敬老院等一线调研督查", "confidence": "plausible", "source_ids": ["S002", "S003"]},
                    {"trait": "pragmatic", "evidence": "强调'项目为王'、以群众满意度为检验标准", "confidence": "plausible", "source_ids": ["S002"]}
                ],
                "speech_themes": ["项目为王", "食品安全", "政绩观", "民生实事"], "management_signals": ["亲自抓重点项目", "重视民生", "优化营商环境"],
                "caveat": "工作风格基于公开报道和讲话表述推断，非私人心理评估"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "截至2026-08未发现吴杰本人纪检处分或负面媒体（任前公示及任内公开报道无负面）。", "date": AS_OF, "confidence": "plausible", "source_ids": []},
                {"type": "context_risk", "description": "虞城县原一级调研员、原常务副县长逯德标 2025-07被查、2026-02被开除党籍移送司法（涉工程项目干预），提示虞城县域系统纪律风险，非吴杰本人。", "date": "2025-07-11", "confidence": "confirmed", "source_ids": ["S005"]}
            ],
            "source_register": [
                {"id": "S001", "title": "河南一批干部任职前公示（吴杰拟任县(市、区)委书记）", "url": "http://renshi.people.com.cn/n1/2026/0420/c139617-40704625.html", "publisher": "人民网/新华网/大河网", "published_at": "2026-04-20", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "吴杰,1976-10,现任柘城县委副书记、县长,拟任虞城县委书记"},
                {"id": "S002", "title": "县委书记吴杰调研食品安全/安置区建设（2026-05）", "url": "https://sq.henance.com/show-63450.html", "publisher": "河南县域经济网/虞城县融媒体中心", "published_at": "2026-05-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认吴杰任虞城县委书记（2026-05起）"},
                {"id": "S003", "title": "吴杰调研重点项目建设（县委书记吴杰、县长蒋验军同场）", "url": "https://c.m.163.com/news/a/L21UGVMB05568W0A.html", "publisher": "虞城县融媒体中心/网易", "published_at": "2026-06-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委书记吴杰、县长蒋验军带队调研重点项目"},
                {"id": "S004", "title": "吴杰（虞城县委书记）百度百科", "url": "https://baike.baidu.com/item/吴杰", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "1976-10河南夏邑人, 宁陵/柘城履历"},
                {"id": "S005", "title": "商丘市纪委监委通报（虞城县原一级调研员等）", "url": "http://www.chbeo.org.cn/article_view.aspx?classid=41&id=9416", "publisher": "营商环境监测中心转载", "published_at": "2026-02", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "虞城原一级调研员逯德标2026-02被开除党籍"}
            ],
            "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "完整履历（宁陵/柘城前早期）与出生定年"},
            "open_questions": [{"priority": "high", "question": "吴杰的出生定年与柘城/宁陵前完整履历？", "why_it_matters": "完整跨县交流线刻画与dedupe", "suggested_queries": ["吴杰 夏邑 简历 宁陵", "吴杰 柘城 常务 简历"], "last_attempted": AS_OF}]
        }
    },
    {
        "id": 2, "name": "蒋验军", "job": "县长",
        "data": {
            "schema_version": "1.0", "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "商丘市", "region": "虞城县", "job": "县委副书记、县长", "task_id": "henan_虞城县", "time_focus": "2021-2026"},
            "identity": {
                "name": "蒋验军", "person_id": "yucheng_jiang_yanjun", "aliases": [], "gender": "男", "ethnicity": "汉族",
                "birth": "1985-08", "birthplace": "", "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": "研究生（法学硕士）", "study_type": "full_time", "source_ids": ["S001"]}],
                "party_join": "中共党员", "work_start": "",
                "dedupe_keys": {"name_birth": "蒋验军_198508", "name_birthplace": "", "official_profile_url": ""}
            },
            "current_status": {"current_post": "县委副书记、县长", "current_org": "虞城县人民政府", "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
            "career_timeline": [
                {"start": "unknown", "end": "2023-11", "org": "虞城县闻集镇", "title": "闻集镇党委书记", "level": "乡科级", "location": "虞城县", "system": "organization", "rank": "正科级", "is_key_promotion": False, "notes": "虞城县委常、闻集镇党委书记（任前公示）", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "2023-11", "org": "中共虞城县委员会", "title": "县委常委", "level": "县处级副职", "location": "虞城县", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "任前公示'现任虞城县委常,闻集镇党委书记'", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2023-12", "end": "2024-03", "org": "虞城县人民政府", "title": "代县长", "level": "县处级正职", "location": "虞城县", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2023-12任代县长", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2024-03-29", "end": "present", "org": "虞城县人民政府", "title": "县长", "level": "县处级正职", "location": "虞城县", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2024-03-29县十六届人大四次会议当选", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "organizations": [
                {"org": "虞城县闻集镇", "role": "党委书记", "period": "未知-2023"},
                {"org": "虞城县人民政府", "role": "代县长/县长", "period": "2023-至今"}
            ],
            "relationships": [
                {"person": "吴杰", "person_id": "yucheng_wu_jie", "relationship_type": "overlap", "strength": "strong", "evidence": "蒋验军（县长）与吴杰（书记）为党政正职搭档，多次同场参会调研。", "overlap_org": "虞城县", "overlap_period": "2026-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
                {"person": "孙虎", "person_id": "yucheng_sun_hu", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "孙虎2022-2023任县长，蒋验军2023-11接任代县长。", "overlap_org": "虞城县人民政府", "overlap_period": "2023-11", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "班春丽", "person_id": "yucheng_ban_chunli", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "班春丽2023-03公示拟任县长候选人未获任、蒋验军2023-11获任，县长职务交替。", "overlap_org": "虞城县人民政府", "overlap_period": "2023", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {"period": "2026-07-13", "domain": "public_security", "achievement_or_event": "主持县政府第78次常务会议，部署安全生产、防汛、消防等。", "role_in_event": "主持", "location": "虞城县", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2024-03", "domain": "economic_development", "achievement_or_event": "作2024年政府工作报告：GDP 357.7亿元居全市第2(+4.6%)、装备制造/新能源/冷链食品/钢卷尺(央视专题)等。", "role_in_event": "作报告", "location": "虞城县", "confidence": "confirmed", "source_ids": ["S004"]}
            ],
            "professional_profile": {
                "primary_specializations": ["政府行政", "项目/产业", "安全生产", "农业农村"], "secondary_specializations": [],
                "career_pattern": "local_ladder", "systems_experience": ["party", "government"], "geographic_pattern": ["河南省商丘市虞城县"],
                "promotion_velocity": {"summary": "从虞城乡镇基层（闻集镇党委书记）跨级升县长，年轻高学历本地干部，2023年底任代县长、2024-03当选。", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [{"trait": "grassroots_oriented", "evidence": "深入乡镇、学校、企业开展安全生产与项目建设调研", "confidence": "plausible", "source_ids": ["S003"]}],
                "speech_themes": ["项目为王", "安全生产", "焦裕禄精神", "农业农村现代化"], "management_signals": ["重视统筹安全与发展"],
                "caveat": "基于公开报道推断，非心理评估"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026-08未发现蒋验军本人纪律或负面信号。", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "公示！商丘一乡党委书记拟任县（市、区）长", "url": "https://www.zysbs.cn/html/zhoubian/sq/2023_11/20/82210829.html", "publisher": "中原新闻网", "published_at": "2023-11-20", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "蒋验军1985-08,研究生法学硕士,虞城县委常、闻集镇党委书记"},
                {"id": "S002", "title": "虞城县第十四次党代会预备会议（2026-06-16）", "url": "https://sq.henance.com/show-63725.html", "publisher": "河南县域经济网", "published_at": "2026-06-16", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "吴杰、蒋验军等任党代会主席团"},
                {"id": "S003", "title": "县长蒋验军主持召开县政府第78次常务会议", "url": "https://sq.henan.com/show-63959.html", "publisher": "河南县域经济网/虞城县融媒体中心", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
                {"id": "S004", "title": "虞城县2025年政府工作报告（县长蒋验军）", "url": "http://www.zgcounty.com/news/67517.html", "publisher": "中国县域", "published_at": "2025-01-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2024年GDP 357.7亿居全市第2"}
            ],
            "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "出生地/闻集镇前完整履历"},
            "open_questions": [{"priority": "high", "question": "蒋验军的出生地及闻集镇前工作经历？", "why_it_matters": "完整身份与履历", "suggested_queries": ["蒋验军 虞城 履历 出生"], "last_attempted": AS_OF}]
        }
    },
    {
        "id": 3, "name": "何玉东", "job": "前任县委书记",
        "data": {
            "schema_version": "1.0", "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "商丘市", "region": "虞城县", "job": "前任县委书记", "task_id": "henan_虞城县", "time_focus": "2021-2026"},
            "identity": {
                "name": "何玉东", "person_id": "yucheng_he_yudong", "aliases": [], "gender": "男", "ethnicity": "汉族",
                "birth": "1968-01", "birthplace": "河南省商丘市梁园区", "native_place": "河南梁园",
                "education": [{"period": "", "institution": "省委党校", "major": "", "degree": "大学", "study_type": "party_school", "source_ids": ["S002"]}],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "何玉东_196801", "name_birthplace": "何玉东_河南商丘梁园", "official_profile_url": ""}
            },
            "current_status": {"current_post": "商丘市政协副主席（原虞城县委书记）", "current_org": "商丘市政协", "administrative_rank": "厅级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S002", "S004"]},
            "career_timeline": [
                {"start": "unknown", "end": "2021-08", "org": "中共梁园区委", "title": "乡镇党委书记、梁园区副区长", "level": "", "location": "商丘市梁园区", "system": "organization", "rank": "区级副职", "is_key_promotion": False, "notes": "梁园区周集乡等乡镇党委书记；梁园区副区长、三级调研员", "confidence": "plausible", "source_ids": ["S002"]},
                {"start": "2021-08", "end": "2022-08", "org": "商丘市工业和信息化局", "title": "副局长", "level": "正处级", "location": "商丘市", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "2021-08任商丘市工信局副局长", "confidence": "confirmed", "source_ids": ["S002"]},
                {"start": "2022-08", "end": "2023-05", "org": "商丘市乡村振兴局", "title": "党组书记、局长", "level": "正处级", "location": "商丘市", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "2022-08任商丘市乡村振兴局党组书记/局长", "confidence": "confirmed", "source_ids": ["S002"]},
                {"start": "2023-05-17", "end": "2026-04", "org": "中共虞城县委员会", "title": "县委书记", "level": "县处级正职", "location": "虞城县", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2023-05-17任虞城县委书记", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
                {"start": "unknown", "end": "present", "org": "商丘市政协", "title": "副主席", "level": "厅级", "location": "商丘市", "system": "party", "rank": "厅级", "is_key_promotion": False, "notes": "任虞城书记期间兼任商丘市政协副主席（2026-04前）", "confidence": "plausible", "source_ids": ["S003", "S004"]}
            ],
            "organizations": [{"org": "中共梁园区委", "role": "乡镇党委书记/副区长", "period": "未知-2021"}, {"org": "商丘市乡村振兴局", "role": "党组书记/局长", "period": "2022-2023"}, {"org": "中共虞城县委员会", "role": "县委书记", "period": "2023-2026"}],
            "relationships": [
                {"person": "吴杰", "person_id": "yucheng_wu_jie", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "何玉东2026-04卸任虞城书记，吴杰接任（前后任交接）。", "overlap_org": "中共虞城县委员会", "overlap_period": "2026", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "蒋验军", "person_id": "yucheng_jiang_yanjun", "relationship_type": "overlap", "strength": "strong", "evidence": "何玉东任虞城书记（2023-2026）期间与县长蒋验军（2024起）搭档。", "overlap_org": "虞城县", "overlap_period": "2024-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]}
            ],
            "governance_record": [{"period": "2026-07-08", "domain": "environment", "achievement_or_event": "民生集中整治、农村供水/养老机构食品安全调研（书记任内相关）", "role_in_event": "带队调研", "location": "虞城县", "confidence": "confirmed", "source_ids": ["S005"]}],
            "professional_profile": {"primary_specializations": ["基层治理", "乡村振兴", "水利基建"], "career_pattern": "cross_county_rotation", "systems_experience": ["party", "government", "organization"], "geographic_pattern": ["商丘市梁园区", "商丘市"], "promotion_velocity": {"summary": "梁园区基层→市直→县处级（县委正职）通话，市直机关到县'配役'组织调动。", "notable_fast_promotions": []}},
            "work_style_and_personality": {"public_style_indicators": [{"trait": "grassroots_oriented", "evidence": "多深入乡镇、农村、养老机构调研", "confidence": "plausible", "source_ids": ["S005"]}], "caveat": "基于公开报道，非心理评估"},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026-08未发现何玉东本人纪律/负面媒体（虞城任内公开报道无负面）。", "date": AS_OF, "confidence": "plausible", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "何玉东任中共虞城县委书记（2023-05-18）", "url": "https://www.zysbs.cn/html/zhoubian/sq/2023_05/18/82197600.html", "publisher": "中原新闻网", "published_at": "2023-05-18", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "任虞城县委书记"},
                {"id": "S002", "title": "商丘市各（区）县现任书记汇总（何玉东）", "url": "https://www.163.com/dy/article/I88AQDO505450VMH.html", "publisher": "网易", "published_at": "2023-06-27", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "梁园区人 1968-01 履历"},
                {"id": "S003", "title": "十三届县委第199次常委会（何玉东主持, 2026-04-09）", "url": "https://sq.henan.com/show-62912.html", "publisher": "河南县域经济网", "published_at": "2026-04-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "虞城县委书记（兼市政协副主席）"},
                {"id": "S004", "title": "虞城县委书记何玉东调研民生实事及养老领域集中整治（2026-07-08）", "url": "https://sq.henan.com/show-59389.html", "publisher": "河南县域经济网", "published_at": "2026-07-08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
                {"id": "S005", "title": "虞城县人民政府官网（县政府领导信息）", "url": "http://www.yuchengxian.gov.cn", "publisher": "虞城县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方站点"}
            ],
            "confidence_summary": {"identity": "plausible", "current_role": "plausible", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "卸任后具体职务的官方表述与出生/学历细节"},
            "open_questions": [{"priority": "high", "question": "何玉东2026-04后具体任职（离任虞城书记后是否为商丘市政协专职副主席）？", "why_it_matters": "人事走向/市对县干部组织真实走向", "suggested_queries": ["何玉东 虞城 卸任 去向", "何玉东 商丘市政协"], "last_attempted": AS_OF}]
        }
    },
]


def main():
    sys.path.insert(0, str(BASE))
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

    for pf in person_files_data:
        person_name = pf["name"]
        job = pf["job"]
        filename = f"{TODAY}-河南省-商丘市-{job}-{person_name}.json"
        filepath = PERSONS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")

    print(f"\nDone. Build complete for {SLUG}.")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")


if __name__ == "__main__":
    main()