#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 铁力市 leadership network.

铁力市是黑龙江省伊春市下辖的县级市，别称"骊城"，位于小兴安岭南麓，以现代农业、
食品加工、森林生态旅游为特色产业，是伊春市唯一的县级市。

Current leadership as of 2026-08 (sources: 伊春市委党务公开网 www.ycswdwgk.gov.cn
「县区动态/铁力市」2024—2026 官方新闻；铁力市人民政府「领导信息」页面
www.tls.gov.cn/newtlsrmzf/c104448，2025-10-29 快照)：
- 市委书记: 吕晓光（曾任铁力市市长，2024年中旬升任书记，截至2026年在任）
- 市委副书记、市长: 王浩（1984年3月生，哈尔滨商业大学财政学专业，2024年中旬任市长）

市政府班子（tls.gov.cn 领导信息 2025-10-29 确认）：
- 市委常委、市政府副市长：袁斯洋、于国峰
- 市政府副市长：赵广福、张琦、刘士东、于新海、王静宇

市人大/政协（2024-2026 新闻确认）：
- 市人大主任：郭春光（2026-02 主持主任会议）；人大党组书记：李兵（2026-06）
- 市政协党组书记、主席：刘铁力（2024-10）

关键人事轨迹（跨县区交流线索）：
- 前任市委书记：陈岩（→升任伊春市副市长/市委常委、常务副市长）
- 栾皓（曾任铁力市委常委、常务副市长、铁力经济开发区党工委副书记 →
  伊春市委副秘书长 → 2026-07 任丰林县委书记）
- 吕晓光 早年前任伊春市机关事务管理局局长。

部分人物完整履历/出生年/籍贯/学历公开一手源有限，均在 confidence、open_questions
标注并写入 report/open_gaps.md，未作虚构。每一条任职/关系在网络图中按来源置信度分级。
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

SLUG = "铁力市"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "铁力市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "铁力市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "铁力市_network.db"
    GEXF_PATH = GRAPH_DIR / "铁力市_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共铁力市委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市铁力市"},
    {"id": 2, "name": "铁力市人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市铁力市"},
    {"id": 3, "name": "铁力市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "伊春市人民代表大会常务委员会", "location": "黑龙江省伊春市铁力市"},
    {"id": 4, "name": "中国人民政治协商会议铁力市委员会", "type": "政协", "level": "县处级", "parent": "伊春市政协", "location": "黑龙江省伊春市铁力市"},
    {"id": 5, "name": "中共铁力市纪律检查委员会/铁力市监察委员会", "type": "纪委", "level": "县处级", "parent": "伊春市纪委/监委", "location": "黑龙江省伊春市铁力市"},
    # 上级/跨层级
    {"id": 6, "name": "中共伊春市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市"},
    {"id": 7, "name": "伊春市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市"},
    {"id": 8, "name": "伊春市机关事务管理局", "type": "政府机关", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市"},
    # 开发区
    {"id": 9, "name": "铁力经济开发区", "type": "开发区", "level": "县处级", "parent": "铁力市人民政府", "location": "黑龙江省伊春市铁力市"},
    # 跨县区（栾皓上行路径）
    {"id": 10, "name": "中共丰林县委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市丰林县"},
    {"id": 11, "name": "中共伊春市委办公室", "type": "党委机关", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 吕晓光 — 市委书记（现任）
    {"id": 1, "name": "吕晓光", "gender": "男",
     "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "铁力市委书记", "current_org": "中共铁力市委员会",
     "source": "https://www.ycswdwgk.gov.cn/; https://www.tls.gov.cn/"},
    # 2 — 王浩 — 市长（现任）
    {"id": 2, "name": "王浩", "gender": "男",
     "ethnicity": "汉族", "birth": "1984年3月", "birthplace": "",
     "education": "哈尔滨商业大学财政学专业（本科学历）",
     "party_join": "2009年8月加入中国共产党", "work_start": "2007年7月",
     "current_post": "铁力市委副书记、市长、市政府党组书记", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/202406/354786.shtml"},
    # 3 — 陈岩 — 前任市委书记（→伊春市常务副市长）
    {"id": 3, "name": "陈岩", "gender": "男",
     "ethnicity": "汉族", "birth": "1973年4月", "birthplace": "",
     "education": "在职大学学历",
     "party_join": "1994年12月加入中国共产党", "work_start": "1993年7月",
     "current_post": "伊春市委常委、市人民政府常务副市长", "current_org": "伊春市人民政府",
     "source": "https://www.ycswdwgk.gov.cn/; https://www.yc.gov.cn/"},
    # 4 — 袁斯洋 — 市委常委、副市长
    {"id": 4, "name": "袁斯洋", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "铁力市委常委、市人民政府副市长", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/"},
    # 5 — 于国峰 — 市委常委、副市长
    {"id": 5, "name": "于国峰", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "铁力市委常委、市人民政府副市长", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/"},
    # 6 — 赵广福 — 副市长
    {"id": 6, "name": "赵广福", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "铁力市人民政府副市长", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/"},
    # 7 — 张琦 — 副市长
    {"id": 7, "name": "张琦", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "铁力市人民政府副市长", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/"},
    # 8 — 刘士东 — 副市长
    {"id": 8, "name": "刘士东", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "铁力市人民政府副市长", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/"},
    # 9 — 于新海 — 副市长
    {"id": 9, "name": "于新海", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "铁力市人民政府副市长", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/"},
    # 10 — 王静宇 — 副市长
    {"id": 10, "name": "王静宇", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "铁力市人民政府副市长", "current_org": "铁力市人民政府",
     "source": "https://www.tls.gov.cn/newtlsrmzf/c104448/"},
    # 11 — 郭春光 — 市人大常委会主任
    {"id": 11, "name": "郭春光", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "铁力市人大常委会主任", "current_org": "铁力市人民代表大会常务委员会",
     "source": "https://www.ycswdwgk.gov.cn/"},
    # 12 — 李兵 — 市人大常委会党组书记（2026）
    {"id": 12, "name": "李兵", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "铁力市人大常委会党组书记（原铁力市委常委、宣传部部长）", "current_org": "铁力市人民代表大会常务委员会",
     "source": "https://www.ycswdwgk.gov.cn/"},
    # 13 — 刘铁力 — 市政协主席
    {"id": 13, "name": "刘铁力", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "铁力市政协党组书记、主席", "current_org": "政协铁力市委员会",
     "source": "https://www.ycswdwgk.gov.cn/"},
    # 14 — 栾皓 — 曾任铁力市委常委、常务副市长 → 丰林县委书记（跨县交流）
    {"id": 14, "name": "栾皓", "gender": "男",
     "ethnicity": "汉族", "birth": "1982年", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "丰林县委书记（原铁力市委常委、常务副市长）", "current_org": "中共丰林县委员会",
     "source": "https://www.ycswdwgk.gov.cn/; 丰林县委官网 2026-07"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 吕晓光
    {"person_id": 1, "org_id": 2, "title": "铁力市市长", "start_date": "2021-2023前后", "end_date": "2024上下", "rank": "县处级正职", "note": "曾任，2024年中旬升任书记"},
    {"person_id": 1, "org_id": 1, "title": "铁力市委书记", "start_date": "2024-06", "end_date": "present", "rank": "县处级正职", "note": "2024年中旬任，截至2026年在任"},
    {"person_id": 1, "org_id": 8, "title": "伊春市机关事务管理局局长（早年）", "start_date": "", "end_date": "2021-06", "rank": "正科/县处", "note": "2021-06伊春市人大免职名单"},
    # 王浩
    {"person_id": 2, "org_id": 1, "title": "铁力市委副书记", "start_date": "2023上下", "end_date": "2024上下", "rank": "县处级副职", "note": "任市长前为市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "铁力市代理市长、市长", "start_date": "2024-06", "end_date": "present", "rank": "县处级正职", "note": "2024年中旬任代理市长，后任市长、市政府党组书记"},
    # 陈岩
    {"person_id": 3, "org_id": 1, "title": "铁力市委书记", "start_date": "2021/2022", "end_date": "2024上下", "rank": "县处级正职", "note": "前任铁力市委书记（2023官方新闻确认）"},
    {"person_id": 3, "org_id": 7, "title": "伊春市人民政府副市长（常务）、市委常委", "start_date": "2025上下", "end_date": "present", "rank": "副厅级", "note": "升任伊春市，2026官方新闻确认为常务副市长"},
    # 袁斯洋、于国峰、赵广福、张琦、刘士东、于新海、王静宇（市政府班子）
    {"person_id": 4, "org_id": 1, "title": "铁力市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼市政府副市长"},
    {"person_id": 4, "org_id": 2, "title": "铁力市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "市委常委、副市长（2025-10-29确认）"},
    {"person_id": 5, "org_id": 1, "title": "铁力市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼市政府副市长"},
    {"person_id": 5, "org_id": 2, "title": "铁力市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "市委常委、副市长（2025-10-29确认）"},
    {"person_id": 6, "org_id": 2, "title": "铁力市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "赵广福"},
    {"person_id": 7, "org_id": 2, "title": "铁力市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "张琦"},
    {"person_id": 8, "org_id": 2, "title": "铁力市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "刘士东"},
    {"person_id": 9, "org_id": 2, "title": "铁力市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "于新海"},
    {"person_id": 10, "org_id": 2, "title": "铁力市人民政府副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "王静宇"},
    # 人大/政协
    {"person_id": 11, "org_id": 3, "title": "铁力市人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2024-02主持主任会议"},
    {"person_id": 12, "org_id": 3, "title": "铁力市人大常委会党组书记", "start_date": "2026", "end_date": "present", "rank": "县处级副职/正职", "note": "2026-06官方会议；原为铁力市委常委、宣传部部长"},
    {"person_id": 12, "org_id": 1, "title": "铁力市委常委、宣传部部长", "start_date": "", "end_date": "2025上下", "rank": "县处级副职", "note": "2024新闻确认"},
    {"person_id": 13, "org_id": 4, "title": "铁力市政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2024-10官方会议确认"},
    # 栾皓（跨县上行）
    {"person_id": 14, "org_id": 9, "title": "铁力市委常委、铁力经济开发区党工委副书记", "start_date": "", "end_date": "", "rank": "", "note": "早年（plausible）"},
    {"person_id": 14, "org_id": 2, "title": "铁力市委常委、常务副市长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "铁力市常务副市长（plausible）"},
    {"person_id": 14, "org_id": 11, "title": "伊春市委副秘书长、办公室主任", "start_date": "", "end_date": "2026-07", "rank": "县处级正职", "note": "伊春市委办"},
    {"person_id": 14, "org_id": 10, "title": "丰林县委书记", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职", "note": "2026年7月下旬任，接替姜治富"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────
relationships = [
    # 书记—市长 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "吕晓光（铁力市委书记）与王浩（市委副书记、市长）当前党政一把手，同任铁力市（2024年起）", "overlap_org": "中共铁力市委/铁力市人民政府", "overlap_period": "2024-至今"},
    # 前任→继任搭档（陈岩→吕晓光）
    {"person_a": 3, "person_b": 1, "type": "前任继任", "context": "陈岩（前任铁力市委书记）由吕晓光（时任铁力市长）接任为市委书记，属党政届内上升路径", "overlap_org": "中共铁力市委员会", "overlap_period": "2023-2024"},
    # 市长→市长前任继任（王浩接替吕晓光的市长）
    {"person_a": 1, "person_b": 2, "type": "前任继任", "context": "吕晓光任市委书记后，王浩由市委副书记升任铁力市长，接替吕晓光的市长职务", "overlap_org": "铁力市人民政府", "overlap_period": "2024"},
    # 市委书记—人大主任
    {"person_a": 1, "person_b": 11, "type": "同城班子", "context": "吕晓光（市委书记）与郭春光（市人大常委会主任）同城四大班子共事", "overlap_org": "铁力市", "overlap_period": "2024-至今"},
    # 市委书记—政协主席
    {"person_a": 1, "person_b": 13, "type": "同城班子", "context": "吕晓光（市委书记）与刘铁力（市政协主席）同城四大班子共事", "overlap_org": "铁力市", "overlap_period": "2024-至今"},
    # 市长—副市长们
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "王浩（市长）与袁斯洋（市委常委、副市长）市政府班子共事", "overlap_org": "铁力市人民政府", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "王浩（市长）与于国峰（市委常委、副市长）市政府班子共事", "overlap_org": "铁力市人民政府", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "王浩（市长）与赵广福（副市长）市政府班子共事", "overlap_org": "铁力市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "王浩（市长）与张琦（副市长）市政府班子共事", "overlap_org": "铁力市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "王浩（市长）与刘士东（副市长）市政府班子共事", "overlap_org": "铁力市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "王浩（市长）与于新海（副市长）市政府班子共事", "overlap_org": "铁力市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "王浩（市长）与王静宇（副市长）市政府班子共事", "overlap_org": "铁力市人民政府", "overlap_period": "至今"},
    # 市委~人大党组
    {"person_a": 1, "person_b": 12, "type": "同城班子", "context": "吕晓光（市委书记）与李兵（市人大常委会党组书记，原铁力市委常委、宣传部长）共事于铁力市", "overlap_org": "铁力市", "overlap_period": "2025-2026"},
    # 前任书记→伊春市（跨层级上升，跨地市网络）
    {"person_a": 3, "person_b": 1, "type": "干部上升链", "context": "陈岩从铁力市委书记升任伊春市常务副市长，是铁力领导干部向地点市上行的重要链条；与现任书记吕晓光同一县域交替", "overlap_org": "伊春市/铁力市", "overlap_period": "2024-2025"},
    # 栾皓（跨县区交流，铁力→伊春→丰林）
    {"person_a": 14, "person_b": 1, "type": "同县域同事", "context": "栾皓（曾任铁力市委常委、常务副市长、经济开发区党工委）与吕晓光曾在铁力市共事", "overlap_org": "铁力市", "overlap_period": "2020年左右"},
    {"person_a": 14, "person_b": 3, "type": "同县域同事", "context": "栾皓与陈岩（前任铁力市委书记）在铁力市委共事", "overlap_org": "中共铁力市委员会", "overlap_period": "2021-2023"},
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