#!/usr/bin/env python3
"""乐山市 领导班子工作关系网络 — 数据构建脚本"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "乐山市"

# ── Persons ──────────────────────────────────────────────────────────
PERSONS = [
    # Top leader
    {"id": 1, "name": "卢军", "gender": "男", "ethnicity": "汉族", "birth": "1971.11",
     "current_post": "市委书记", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swsj/755778490769477.html"},

    # Deputy Party Secretaries
    {"id": 2, "name": "赵迎春", "gender": "男", "ethnicity": "汉族", "birth": "1970.06",
     "current_post": "市委副书记、市长", "current_org": "中共乐山市委/市政府",
     "source": "https://www.leshan.gov.cn/lsswszf/zwgksz/698695416266821.html"},
    {"id": 3, "name": "文甦", "gender": "男", "ethnicity": "汉族", "birth": "1973.02",
     "current_post": "市委副书记", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swfsj/697628415172677.html"},

    # Standing Committee members
    {"id": 4, "name": "陈杰", "gender": "男", "ethnicity": "汉族", "birth": "1976.11",
     "current_post": "市委常委、市纪委书记、市监委主任", "current_org": "中共乐山市委/市纪委",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/764972606890053.html"},
    {"id": 5, "name": "谭焰", "gender": "男", "ethnicity": "汉族", "birth": "1969.10",
     "current_post": "市委常委、政法委书记", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/697630935720005.html"},
    {"id": 6, "name": "文春雷", "gender": "男", "ethnicity": "汉族", "birth": "1979.01",
     "current_post": "市委常委、组织部部长、党校校长", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/697630859173957.html"},
    {"id": 7, "name": "雷建新", "gender": "男", "ethnicity": "汉族", "birth": "1970.04",
     "current_post": "市委常委、市直机关工委书记", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/697630628315205.html"},
    {"id": 8, "name": "黄秀航", "gender": "男", "ethnicity": "汉族", "birth": "1981.10",
     "current_post": "市委常委、常务副市长", "current_org": "中共乐山市委/市政府",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/697630545436741.html"},
    {"id": 9, "name": "吕红波", "gender": "男", "ethnicity": "汉族", "birth": "1977.11",
     "current_post": "市委常委、军分区政委", "current_org": "乐山军分区",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/697630429757509.html"},
    {"id": 10, "name": "许天毅", "gender": "男", "ethnicity": "汉族", "birth": "1970.07",
     "current_post": "市委常委、宣传部部长", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/734879571431493.html"},
    {"id": 11, "name": "吴小怡", "gender": "女", "ethnicity": "汉族", "birth": "1974.11",
     "current_post": "市委常委、统战部部长", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/804252890935365.html"},
    {"id": 12, "name": "冯彬", "gender": "男", "ethnicity": "汉族", "birth": "1973.05",
     "current_post": "市委常委、副市长", "current_org": "中共乐山市委/市政府",
     "source": "https://www.leshan.gov.cn/lsswszf/swcw/697629832298565.html"},

    # Other Vice Mayors
    {"id": 13, "name": "张春刚", "gender": "男", "ethnicity": "汉族", "birth": "1970.10",
     "current_post": "副市长、市公安局局长", "current_org": "乐山市人民政府",
     "source": "https://www.leshan.gov.cn/lsswszf/fsz/698696248774725.html"},
    {"id": 14, "name": "毛剑", "gender": "男", "ethnicity": "汉族", "birth": "1967.05",
     "current_post": "副市长", "current_org": "乐山市人民政府",
     "source": "https://www.leshan.gov.cn/lsswszf/fsz/698696378658885.html"},
    {"id": 15, "name": "张国清", "gender": "男", "ethnicity": "汉族", "birth": "1967.07",
     "current_post": "副市长", "current_org": "乐山市人民政府",
     "source": "https://www.leshan.gov.cn/lsswszf/fsz/698696570863685.html"},
    {"id": 16, "name": "廖沂", "gender": "男", "ethnicity": "汉族", "birth": "1972.11",
     "current_post": "副市长", "current_org": "乐山市人民政府",
     "source": "https://www.leshan.gov.cn/lsswszf/fsz/698696986529861.html"},
    {"id": 17, "name": "徐岳泉", "gender": "男", "ethnicity": "汉族", "birth": "1972.02",
     "current_post": "副市长、犍为县委书记", "current_org": "乐山市人民政府",
     "source": "https://www.leshan.gov.cn/lsswszf/fsz/810541026099269.html"},
    {"id": 18, "name": "刘文斌", "gender": "男", "ethnicity": "汉族", "birth": "1976.10",
     "current_post": "副市长", "current_org": "乐山市人民政府",
     "source": "https://www.leshan.gov.cn/lsswszf/fsz/822553765851205.html"},

    # Secretaries
    {"id": 19, "name": "高志飞", "gender": "男", "ethnicity": "汉族", "birth": "1974.05",
     "current_post": "市委秘书长", "current_org": "中共乐山市委",
     "source": "https://www.leshan.gov.cn/lsswszf/swmsz/697631196713029.html"},
    {"id": 20, "name": "兰波", "gender": "男", "ethnicity": "汉族", "birth": "1975.06",
     "current_post": "市政府秘书长", "current_org": "乐山市人民政府",
     "source": "https://www.leshan.gov.cn/lsswszf/msz/698697139019845.html"},
]

# ── 机构 ──────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共乐山市委", "type": "党委", "level": "地市级", "parent": "中共四川省委", "location": "乐山市"},
    {"id": 2, "name": "乐山市人民政府", "type": "政府", "level": "地市级", "parent": "四川省人民政府", "location": "乐山市"},
    {"id": 3, "name": "乐山市纪律检查委员会", "type": "纪委", "level": "地市级", "parent": "中共乐山市委/四川省纪委", "location": "乐山市"},
    {"id": 4, "name": "乐山市监察委员会", "type": "监察", "level": "地市级", "parent": "乐山市人大/四川省监委", "location": "乐山市"},
    {"id": 5, "name": "乐山军分区", "type": "军队", "level": "师级", "parent": "四川省军区", "location": "乐山市"},
    {"id": 6, "name": "乐山市公安局", "type": "政府", "level": "地市级", "parent": "乐山市人民政府", "location": "乐山市"},
]

# ── 任职关系（dict格式，符合schema要求） ─────────────────────
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼市长"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "专职副书记"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "市纪委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "市监委主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼党校校长"},
    {"person_id": 7, "org_id": 1, "title": "市委常委、市直机关工委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府党组副书记"},
    {"person_id": 9, "org_id": 1, "title": "市委常委、军分区政委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "军分区政委", "start_date": "", "end_date": "", "rank": "正师级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市公安局局长"},
    {"person_id": 13, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民进会员"},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼犍为县委书记"},
    {"person_id": 18, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "市委秘书长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记+市长搭班子", "overlap_org": "乐山市委/市政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 3, "type": "同事", "context": "两位市委副书记", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "市长+常务副市长", "overlap_org": "乐山市政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委+市纪委", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委+政法委", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委+组织部", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记+常务副市长", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "市委+宣传部", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "市委+统战部", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 12, "type": "同事", "context": "两位常委副市长", "overlap_org": "市政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 15, "type": "上下级", "context": "常务副市长+副市长", "overlap_org": "市政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 13, "type": "上下级", "context": "常务副市长+副市长", "overlap_org": "市政府", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 11, "type": "同事", "context": "组织部长+统战部长", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 5, "type": "同事", "context": "纪委书记+政法委书记", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 10, "type": "同事", "context": "纪委书记+宣传部长", "overlap_org": "乐山市委", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 1, "type": "上下级", "context": "市直机关工委书记+市委书记", "overlap_org": "乐山市委", "overlap_period": "至今"},
]

run_build(
    slug=SLUG,
    persons=PERSONS,
    organizations=ORGANIZATIONS,
    positions=POSITIONS,
    relationships=RELATIONSHIPS,
    db_path=DATABASE_DIR / f"{SLUG}_network.db",
    gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
    overwrite=True,
)
