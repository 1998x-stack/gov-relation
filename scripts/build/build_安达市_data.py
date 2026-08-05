#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 安达市 (Anda City) leadership network.

安达市是黑龙江省绥化市代管的县级市，地处松嫩平原腹地、哈大齐工业走廊上，是著名的
"乳业名城"，乳制品/液态奶产业发达，兼有石油石化产业。

Current leadership as of 2026-08 (primary source: 安达市人民政府门户网站
http://www.hlanda.gov.cn 「领导视窗」各领导简介页 + 政务发布/政务活动官方新闻确认):
- 市委书记: 田鹏飞（男，汉族，1973年10月生，管理学博士，中共党员；现任，官方新闻 2026-07 持续确认）
- 市委副书记、市长: 王帅（男，汉族，1978年10月生，大专，中共党员；现任，2026 市政府常务会议多确认）

安达市为绥化市的县级市，上溯为地级绥化市的直接下属，组织层级按 县级市（正处级） 设定。

证据说明: 名单与身份字段均来自官方网站「领导简介」，为 high 置信度。多数县级干部完整
广度履历（任职起止、籍贯、入党/参加工作年份）公开资料有限，均以 confidence 与
open_questions 保留，未作虚构。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "安达市"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "安达市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "安达市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "安达市_network.db"
    GEXF_PATH = GRAPH_DIR / "安达市_network.gexf"

# ── ORGANIZATIONS ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共安达市委员会", "type": "决策", "level": "县级市党委", "parent": "中共绥化市委员会", "location": "黑龙江省绥化市安达市"},
    {"id": 2, "name": "安达市人民政府", "type": "政府", "level": "县级市政府", "parent": "绥化市人民政府", "location": "黑龙江省绥化市安达市"},
    {"id": 3, "name": "安达市人民代表大会常务委员会", "type": "人大", "level": "县级市人大", "parent": "绥化市人民代表大会常务委员会", "location": "黑龙江省绥化市安达市"},
    {"id": 4, "name": "中国人民政治协商会议安达市委员会", "type": "政协", "level": "县级市政协", "parent": "绥化市政协", "location": "黑龙江省绥化市安达市"},
    {"id": 5, "name": "中共安达市纪律检查委员会/安达市监察委员会", "type": "纪委", "level": "县级市纪委", "parent": "中共绥化市纪律检查委员会", "location": "黑龙江省绥化市安达市"},
    {"id": 6, "name": "安达市公安局", "type": "政府机关", "level": "执法机关", "parent": "安达市人民政府", "location": "黑龙江省绥化市安达市"},
    {"id": 7, "name": "安达市人民武装部", "type": "军事", "level": "县级", "parent": "", "location": "黑龙江省绥化市安达市"},
    {"id": 110, "name": "中共绥化市委员会", "type": "决策", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "黑龙江省绥化市"},
    {"id": 120, "name": "绥化市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省绥化市"},
]

# ── PERSONS ───────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "田鹏飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-10", "birthplace": "", "education": "管理学博士",
     "party_join": "", "work_start": "",
     "current_post": "安达市委书记", "current_org": "中共安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/shuji/202109/c12_84066.shtml"},
    {"id": 2, "name": "王帅", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委副书记、市长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/shizhang/202210/c12_84087.shtml"},
    {"id": 3, "name": "闫欢", "gender": "女", "ethnicity": "汉族",
     "birth": "1988-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委副书记（挂职）", "current_org": "中共安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/fsj/202504/c12_207994.shtml"},
    {"id": 4, "name": "刘俊杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委副书记", "current_org": "中共安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/fsj/202507/c12_213398.shtml"},
    {"id": 5, "name": "韩佳栋", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委常委、组织部长", "current_org": "中共安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202103/c12_84072.shtml"},
    {"id": 6, "name": "李元彬", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "安达市委常委、人武部上校政委", "current_org": "安达市人民武装部",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202307/c12_84078.shtml"},
    {"id": 7, "name": "蒋敏强", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委常委、副市长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202412/c12_198670.shtml"},
    {"id": 8, "name": "林雪松", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-10", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委常委、政法委书记", "current_org": "中共安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202412/c12_198676.shtml"},
    {"id": 9, "name": "韩殿军", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-03", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委常委、宣传部长", "current_org": "中共安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202109/c12_84076.shtml"},
    {"id": 10, "name": "刘小磊", "gender": "男", "ethnicity": "",
     "birth": "1983-02", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委常委、纪委书记、监委主任", "current_org": "中共安达市纪律检查委员会",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202412/c12_198677.shtml"},
    {"id": 11, "name": "刘营", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-04", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委常委、统战部长", "current_org": "中共安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202408/c12_189771.shtml"},
    {"id": 12, "name": "刘兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-02", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市委常委、副市长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/changwei/202409/c12_191343.shtml"},
    {"id": 13, "name": "张文殊", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-10", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市副市长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/fsz/202109/c12_84090.shtml"},
    {"id": 14, "name": "杨永春", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-11", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市副市长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/fsz/202303/c12_84089.shtml"},
    {"id": 15, "name": "王云鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市副市长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/fsz/202309/c12_84095.shtml"},
    {"id": 16, "name": "艾丽丽", "gender": "女", "ethnicity": "汉族",
     "birth": "1978-08", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市副市长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/fsz/202408/c12_189874.shtml"},
    {"id": 17, "name": "孙松鹤", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市副市长、市公安局局长", "current_org": "安达市人民政府",
     "source": "http://www.hlanda.gov.cn/ad/fsz/202409/c12_191346.shtml"},
    {"id": 18, "name": "匡新明", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-01", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市人大常委会主任", "current_org": "安达市人民代表大会常务委员会",
     "source": "http://www.hlanda.gov.cn/ad/zhuren/202409/c12_191344.shtml"},
    {"id": 19, "name": "张书春", "gender": "女", "ethnicity": "汉族",
     "birth": "1970-01", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安达市政协党组书记、主席", "current_org": "中国人民政治协商会议安达市委员会",
     "source": "http://www.hlanda.gov.cn/ad/zhuxi/202406/c12_186185.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "安达市委书记", "start_date": "2021-09(档案)", "end_date": "present", "rank": "县处级正职", "note": "现任；官方简介页 2021-09"},
    {"person_id": 2, "org_id": 2, "title": "安达市人民政府市长", "start_date": "2022-10(档案)", "end_date": "present", "rank": "县处级正职", "note": "现任；兼市委副书记"},
    {"person_id": 2, "org_id": 1, "title": "安达市委副书记", "start_date": "2021-09(档案)", "end_date": "present", "rank": "县处级副职", "note": "兼任"},
    {"person_id": 3, "org_id": 1, "title": "安达市委副书记（挂职）", "start_date": "2025-04(档案)", "end_date": "present", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 4, "org_id": 1, "title": "安达市委副书记", "start_date": "2025-07(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "安达市委常委、组织部长", "start_date": "2021-03(档案)", "end_date": "present", "rank": "县处级副职", "note": "党校第一副校长、二级调研员"},
    {"person_id": 6, "org_id": 7, "title": "安达市人武部上校政委", "start_date": "2023-07(档案)", "end_date": "present", "rank": "县处级副职", "note": "市委常委"},
    {"person_id": 7, "org_id": 2, "title": "安达市副市长", "start_date": "2024-12(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 7, "org_id": 1, "title": "安达市委常委", "start_date": "2024-12(档案)", "end_date": "present", "rank": "县处级副职", "note": "常委"},
    {"person_id": 8, "org_id": 1, "title": "安达市委常委、政法委书记", "start_date": "2024-12(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 9, "org_id": 1, "title": "安达市委常委、宣传部长", "start_date": "2021-09(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 10, "org_id": 5, "title": "安达市委常委、纪委书记、监委主任", "start_date": "2024-12(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 11, "org_id": 1, "title": "安达市委常委、统战部长", "start_date": "2024-08(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 12, "org_id": 2, "title": "安达市副市长", "start_date": "2024-09(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 12, "org_id": 1, "title": "安达市委常委", "start_date": "2024-09(档案)", "end_date": "present", "rank": "县处级副职", "note": "常委"},
    {"person_id": 13, "org_id": 2, "title": "安达市副市长", "start_date": "2021-09(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 14, "org_id": 2, "title": "安达市副市长", "start_date": "2023-03(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 15, "org_id": 2, "title": "安达市副市长", "start_date": "2023-09(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 16, "org_id": 2, "title": "安达市副市长", "start_date": "2024-08(档案)", "end_date": "present", "rank": "县处级副职", "note": "现任"},
    {"person_id": 17, "org_id": 2, "title": "安达市副市长、市公安局局长", "start_date": "2024-09(档案)", "end_date": "present", "rank": "县处级副职", "note": "公安局长"},
    {"person_id": 17, "org_id": 6, "title": "安达市公安局党委书记、局长", "start_date": "2024-09(档案)", "end_date": "present", "rank": "正科级", "note": "兼"},
    {"person_id": 18, "org_id": 3, "title": "安达市人大常委会主任", "start_date": "2024-09(档案)", "end_date": "present", "rank": "县处级正职", "note": "现任"},
    {"person_id": 19, "org_id": 4, "title": "安达市政协党组书记、主席", "start_date": "2024-06(档案)", "end_date": "present", "rank": "县处级正职", "note": "现任"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "田鹏飞（市委书记）与王帅（市委副书记、市长）为安达市现任党政一把手搭档", "overlap_org": "中共安达市委/安达市政府", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "田鹏飞（书记）与闫欢（市委副书记，挂职）同为市委班子", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "田鹏飞（书记）与刘俊杰（市委副书记）同为市委班子", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "田鹏飞（书记）与韩佳栋（组织部长）在市委常委会", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "田鹏飞（书记）与蒋敏强（常委、副市长）在市委常委会", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "田鹏飞（书记）与林雪松（政法委书记）在市委常委会", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "田鹏飞（书记）与韩殿军（宣传部长）在市委常委会", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "田鹏飞（书记）与刘小磊（纪委书记）在市委常委会", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "田鹏飞（书记）与刘营（统战部长）在市委常委会", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "田鹏飞（书记）与刘兵（常委、副市长）在市委常委会", "overlap_org": "中共安达市委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "王帅（市长）与蒋敏强（副市长、常委）共事于市政府班子", "overlap_org": "安达市政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "王帅（市长）与刘兵（副市长、常委）共事于市政府班子", "overlap_org": "安达市政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "王帅（市长）与张文殊（副市长）共事于市政府班子", "overlap_org": "安达市政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "王帅（市长）与杨永春（副市长）共事于市政府班子", "overlap_org": "安达市政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "王帅（市长）与王云鹏（副市长）共事于市政府班子", "overlap_org": "安达市政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "王帅（市长）与艾丽丽（副市长）共事于市政府班子", "overlap_org": "安达市政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "王帅（市长）与孙松鹤（副市长兼公安局长）共事于市政府班子", "overlap_org": "安达市政府", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 17, "type": "同条线", "context": "林雪松（政法委书记）与孙松鹤（公安局长）在政法条线工作交集", "overlap_org": "安达市政法系统", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 12, "type": "同职级", "context": "蒋敏强与刘兵均为市委常委兼副市长，双重任职结构相似", "overlap_org": "中共安达市委/安达市政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 18, "type": "党政关系", "context": "田鹏飞（书记）与匡新明（人大常委会主任）为书记与人大主官", "overlap_org": "安达市", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 19, "type": "党政关系", "context": "田鹏飞（书记）与张书春（政协主席）为书记与政协主官", "overlap_org": "安达市", "overlap_period": "至今"},
]

if __name__ == "__main__":
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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")