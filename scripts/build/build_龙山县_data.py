#!/usr/bin/env python3
"""
Build script for 龙山县 (Longshan County), 湘西土家族苗族自治州, 湖南省.
Current as of 2026-08.

Key confirmed findings (source: Baidu PTAL search index over 龙山新闻网/湘西党建/人民日报/新湖南/腾讯网,
accessed 2026-08-06):

- 县委书记: 吴光文 (appointed 2026-04-13; 湖南汨罗人 b.1974-02, 研究生, 1997 湖南师大化学教育;
   历任屈原管理区(黄金办事处纪委/凤凰乡乡长/黄金乡书记)→临湘市委常委组织部长→岳阳县委常委常务副县长→岳阳县委副书记县长(2021))
- 县长: 彭礼 (代理县长; 县委副书记; confirmed 2026-07-29 龙山县第十四次党代会 以代理县长身份出席;
   2026-05-19 湘西州委任前公示 '拟提名为县市人民政府正职候选人'; 土家族 b.1985-03 在职研究生法学硕士)
- 前县委书记: 时荣芬 (2022-01 ~ 2026-04; 女 苗族 湖南花垣 b.1977-01; 前湘西州文广局局长; 去向未核实)
- 前县委书记/被查: 刘冬生 (2019~2022-01; 湖南衡南 b.1977-09 工学博士; 2022-01 升湘西州副州长; 2025-05-12 被查,
   涉嫌严重违纪违法主动交代, 中央纪委国家监委/湖南省纪委监委通报) — MAJOR RISK SIGNAL
- 前县长: 周胜益 (2022-03 ~ 约2026-04; 苗族 b.1972-09 湖南保靖; 2022-02-26 任龙山县委副书记, 2022-03-08 代理县长,
   2022-03-10 任县长; 2026 年中离任, 去向未核实)
- 现任班子(部分): 县委副书记 黎新松(早); 县委常委、常务副县长 向恿文; 县纪委书记/监委主任 张兵(前 龙江);
  委员\人武部政委 刘建飞; 县人大主任 周大钊(前 黄勇); 县政协主席 杨波; 副县长 龚彪 等

DATA INTEGRITY NOTICE:
- Web access degraded (Exa rate-limit; Baidu gov.org host WAF-412; r.jina.ai timeout; Baidu search captcha after
  heavy use). Core face (书记/县长) CONFIRMED from multiple independent official/news reports.
- Full career resumes, birth/party-join/work-start for the disclosed individuals are PARTIAL; gaps are
  encoded explicitly with confidence and open_questions rather than fabricated.
- 刘冬生 (原龙山县委书记、湘西州副州长) 2025-05-12 被查 is confirmed (中央纪委国家监委/湖南省纪委监委通报).

Sources:
- 人民日报/湘西州委组织部: 吴光文任龙山县委书记 (2026-04-13)
- 龙山新闻网: 2026龙山县武装工作会 (2026-04-09, 彭礼主持、周大钊/杨波/刘建飞出席)
- 湘乡州委组织部任免公示 (2026-05-19): 彭礼拟任县长
- 龙山新闻网: 龙山县第十四次党代会 彭礼代理县长 (2026-07-29)
- 百度百科: 吴光文/刘冬生 词条
- 新浪财经: 刘冬生被查 (2025-05-12)
"""

import sys
import os
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve()
for _ in _REPO_ROOT.parents:
    if (_ / "gov_relation").is_dir():
        _REPO_ROOT = _
        break
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.gexf import GEXFBuilder
import sqlite3

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now().strftime("%Y-%m-%d")

persons = [
    {
        "id": 1, "name": "吴光文", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-04", "birthplace": "湖南省汨罗市",
        "education": "研究生（湖南师范大学化学教育专业本科）", "party_join": "1994-11", "work_start": "1997-07",
        "current_post": "龙山县委书记", "current_org": "中共龙山县委员会",
        "source": "百度百科 / 人民日报-湘西党建(2026-04-13)",
    },
    {
        "id": 2, "name": "彭礼", "gender": "男", "ethnicity": "土家族",
        "birth": "1985-03", "birthplace": "湖南省（籍贯待核）",
        "education": "在职研究生，法学硕士", "party_join": "", "work_start": "",
        "current_post": "龙山县委副书记、代县长", "current_org": "龙山县人民政府",
        "source": "湘西州委任免公示(2026-05-19) / 龙山新闻网(2026-07-29)",
    },
    {
        "id": 3, "name": "时荣芬", "gender": "女", "ethnicity": "苗族",
        "birth": "1977-01", "birthplace": "湖南省花垣县",
        "education": "在职大学", "party_join": "2000-06", "work_start": "1996-07",
        "current_post": "龙山县委原书记（去向待核）", "current_org": "中共龙山县委员会（已卸任）",
        "source": "湘西州文广局 / 新湖南(2022-01-20) / 闪电新闻",
    },
    {
        "id": 4, "name": "周胜益", "gender": "男", "ethnicity": "苗族",
        "birth": "1972-09", "birthplace": "湖南省保靖县",
        "education": "中央党校大学", "party_join": "1997-05", "work_start": "1992-07",
        "current_post": "龙山县委原县长（去向待核）", "current_org": "龙山县人民政府（已卸任）",
        "source": "百度百科 / 新湖南/红网(2022-02-26, 2022-03-08)",
    },
    {
        "id": 5, "name": "刘冬生", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-09", "birthplace": "湖南省衡南县",
        "education": "博士研究生，工学博士", "party_join": "1998-03", "work_start": "2005-07",
        "current_post": "湘西州原副州长（2025-05 被查）", "current_org": "湘西土家族苗族自治州人民政府（被查）",
        "source": "百度百科 / 中央纪委国家监委官网 / 新浪(2025-05-12)",
    },
    {
        "id": 6, "name": "黎新松", "gender": "男", "ethnicity": "土家族",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委原副书记（2022）", "current_org": "中共龙山县委员会",
        "source": "红网(2021-07-31 当选十三届县委副书记) / 龙山红星网(2023-03)",
    },
    {
        "id": 7, "name": "向柏文", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委常委、常务副县长", "current_org": "龙山县人民政府",
        "source": "龙山新闻网(医保参保缴费会议 2025-12-31) / 人民网 税务局(2026-02-28)",
    },
    {
        "id": 8, "name": "张兵", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委常委、县纪委书记、县监委主任", "current_org": "中共龙山县纪律检查委员会",
        "source": "新湖南 法治报(2025-06-14 群众学深纠治集中整治)",
    },
    {
        "id": 9, "name": "龙志勇", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委领导（副职待核）", "current_org": "中共龙山县委员会",
        "source": "龙山县委警示教育会名单(2025-06)",
    },
    {
        "id": 10, "name": "杨甜", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委领导（宣传？组织？待核）", "current_org": "中共龙山县委员会",
        "source": "龙山县委警示教育会名单(2025-06) / 春节离退休干部座谈会(2026-02)",
    },
    {
        "id": 11, "name": "周大钊", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县人大常委会主任", "current_org": "龙山县人民代表大会常务委员会",
        "source": "龙山新闻网 武装工作会(2026-04-09)",
    },
    {
        "id": 12, "name": "杨波", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "县政协主席", "current_org": "中国人民政治协商会议龙山县委员会",
        "source": "龙山新闻网 武装工作会(2026-04-09) / 龙山红星网(2023-03)",
    },
    {
        "id": 13, "name": "黄勇", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县人大常委会原主任（周大钊前任）", "current_org": "龙山县人民代表大会常务委员会",
        "source": "龙山新闻(2022-03 / 2023-03)",
    },
    {
        "id": 14, "name": "李延堃", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委原常务副县长（2022）", "current_org": "龙山县人民政府",
        "source": "龙山新闻 人大常委会(2022-03-08) / 清廉龙山(2023-03)",
    },
    {
        "id": 15, "name": "龙江", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委原纪委书记、监委主任（2022-2024）", "current_org": "中共龙山县纪律检查委员会",
        "source": "龙山新闻(2022-03-08) / 清廉龙山(2023-03) / 十三届四次全会(2024)",
    },
    {
        "id": 16, "name": "龚彪", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县副县长", "current_org": "龙山县人民政府",
        "source": "龙山新闻网 医保参保缴费(2025-12-31)",
    },
    {
        "id": 17, "name": "刘建飞", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "龙山县委常委、县人武部政委", "current_org": "龙山县人民武装部",
        "source": "龙山新闻网 武装工作会(2026-04-09) / 警示教育会(2025-06)",
    },
]

organizations = [
    {"id": 1, "name": "中共龙山县委员会", "type": "county_party", "level": "county",
     "parent": "中共湘西土家族苗族自治州委员会", "location": "龙山县"},
    {"id": 2, "name": "龙山县人民政府", "type": "county_gov", "level": "county",
     "parent": "湘西土家族苗族自治州人民政府", "location": "龙山县"},
    {"id": 3, "name": "中共湘西土家族苗族自治州委员会", "type": "prefecture_party", "level": "prefecture",
     "parent": "中共湖南省委员会", "location": "吉首市"},
    {"id": 4, "name": "湘西土家族苗族自治州人民政府", "type": "prefecture_gov", "level": "prefecture",
     "parent": "湖南省人民政府", "location": "吉首市"},
    {"id": 5, "name": "中共岳阳县委员会", "type": "county_party", "level": "county",
     "parent": "中共岳阳市委员会", "location": "岳阳县"},
    {"id": 6, "name": "岳阳县人民政府", "type": "county_gov", "level": "county",
     "parent": "岳阳市人民政府", "location": "岳阳县"},
    {"id": 7, "name": "中共临湘市委员会", "type": "county_party", "level": "county",
     "parent": "中共岳阳市委员会", "location": "临湘市"},
    {"id": 8, "name": "屈原管理区", "type": "development_zone", "level": "township",
     "parent": "岳阳市", "location": "汨罗市/屈原管理区"},
    {"id": 9, "name": "中共龙山县纪律检查委员会", "type": "county_discipline", "level": "county",
     "parent": "中共龙山县委员会", "location": "龙山县"},
    {"id": 10, "name": "龙山县人民代表大会常务委员会", "type": "county_people_congress", "level": "county",
     "parent": "湘西土家族苗族自治州人大常委会", "location": "龙山县"},
    {"id": 11, "name": "中国人民政治协商会议龙山县委员会", "type": "county_cppcc", "level": "county",
     "parent": "湘西土家族苗族自治州政协", "location": "龙山县"},
    {"id": 12, "name": "龙山县人民武装部", "type": "county_military", "level": "county",
     "parent": "吉首军分区", "location": "龙山县"},
]

positions = [
    # 吴光文
    {"person_id": 1, "org_id": 1, "title": "龙山县委书记", "start_date": "2026-04", "end_date": "", "rank": "正处级",
     "note": "2026-04-13 干部大会宣布任龙山县委书记"},
    {"person_id": 1, "org_id": 5, "title": "岳阳县委副书记、县长", "start_date": "2021-07", "end_date": "2026", "rank": "正处级",
     "note": "2021-07-13 提名为县长候选人；2026 辞去县长"},
    {"person_id": 1, "org_id": 6, "title": "岳阳县委常委、常务副县长", "start_date": "", "end_date": "2021-07", "rank": "副处级",
     "note": "职位起止待核(gap)"},
    {"person_id": 1, "org_id": 7, "title": "临湘市委常委、组织部长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "担任时间待核(gap)"},
    {"person_id": 1, "org_id": 8, "title": "屈原管理区 黄金乡党委书记/凤凰乡乡长/黄金办事处纪委书记", "start_date": "1997-07", "end_date": "", "rank": "乡科级",
     "note": "湖南师范大学化学教育专业毕业后在屈原管理区多岗位历练"},
    # 彭礼
    {"person_id": 2, "org_id": 2, "title": "龙山县代县长", "start_date": "2026-07", "end_date": "", "rank": "正处级",
     "note": "2026-05-19 湘西州委公示拟任县长正职候选人；2026-07 为代理县长"},
    {"person_id": 2, "org_id": 1, "title": "龙山县委副书记（正处级）", "start_date": "", "end_date": "2026-07", "rank": "正处级",
     "note": "任副书记起止待核(gap)"},
    # 时荣芬
    {"person_id": 3, "org_id": 1, "title": "龙山县委书记", "start_date": "2022-01", "end_date": "2026-04", "rank": "正处级",
     "note": "2022-01-20 任书记；2026-04 由吴光文接任"},
    {"person_id": 3, "org_id": 2, "title": "龙山县县长（前任）", "start_date": "", "end_date": "2022-03", "rank": "正处级",
     "note": "2022-03-10 辞去县长"},
    {"person_id": 3, "org_id": 3, "title": "湘西州文广局（前任）", "start_date": "", "end_date": "2022-01", "rank": "正处级",
     "note": "任龙山书记前任州文广局局长"},
    # 周胜益
    {"person_id": 4, "org_id": 2, "title": "龙山县县长", "start_date": "2022-03", "end_date": "2026", "rank": "正处级",
     "note": "2022-03-08 代理县长，2022-03-10 承接；约2026年卸任"},
    {"person_id": 4, "org_id": 1, "title": "龙山县委副书记", "start_date": "2022-02", "end_date": "", "rank": "正处级",
     "note": "2022-02-26 任县委副书记"},
    # 刘冬生 (被查)
    {"person_id": 5, "org_id": 4, "title": "湘西州副州长", "start_date": "2022-01", "end_date": "2025-05", "rank": "副厅级",
     "note": "2025-05-12 主动交代问题被查"},
{"person_id": 5, "org_id": 1, "title": "龙山县委书记", "start_date": "2019", "end_date": "2022-01", "rank": "正处级",
     "note": "2019 任县委书记，2022-01 卸任升湘西州副州长"},
    {"person_id": 5, "org_id": 2, "title": "龙山县县长（前任）", "start_date": "2016", "end_date": "2019", "rank": "正处级",
     "note": "2016 任龙山县委副书记、县长"},
    # 黎新松
    {"person_id": 6, "org_id": 1, "title": "龙山县委副书记", "start_date": "2021-07", "end_date": "2023", "rank": "正处级",
     "note": "2021-07-31 十三届县委副书记；2023 后未再列名(gap)"},
    # 向柏文
    {"person_id": 7, "org_id": 2, "title": "龙山县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "2025-12 医保/税务会议在任"},
    # 张兵
    {"person_id": 8, "org_id": 9, "title": "县纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "2025-06 在任"},
    # 周大钊
    {"person_id": 11, "org_id": 10, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "2026-04 在任"},
    # 杨波
    {"person_id": 12, "org_id": 11, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "2026-04 在任"},
    # 黄勇 (原人大主任)
    {"person_id": 13, "org_id": 10, "title": "县人大常委会主任", "start_date": "2022-03", "end_date": "", "rank": "正处级",
     "note": "2022-03-08 仍在任；后由周大钊接任"},
    # 李延堃
    {"person_id": 14, "org_id": 2, "title": "龙山县委常务副县长", "start_date": "", "end_date": "2023", "rank": "副处级",
     "note": "2022-03 在任"},
    # 龙江
    {"person_id": 15, "org_id": 9, "title": "县纪委书记、监委主任", "start_date": "", "end_date": "2024", "rank": "副处级",
     "note": "2022-2024 在任"},
    # 龚彪
    {"person_id": 16, "org_id": 2, "title": "龙山县副县长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "2025-12 在任"},
    # 刘建飞
    {"person_id": 17, "org_id": 12, "title": "县委常委、县人武部政委", "start_date": "", "end_date": "", "rank": "副师",
     "note": "2026-04 在任"},
]

relationships = [
    # 书记-县长 搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "吴光文(书记)与彭礼(代县长)为2026年龙山党政主官搭档",
     "overlap_org": "中共龙山县委员会", "overlap_period": "2026-04起"},
    # 书记继任链
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "context": "时荣芬 与 周胜益：2022-01时荣芬任书记、周胜益接任县长",
     "overlap_org": "龙山县人民政府", "overlap_period": "2022-03"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "吴光文 接任 时荣芬 任龙山县委书记（2026-04-13）",
     "overlap_org": "中共龙山县委员会", "overlap_period": "2026-04"},
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor",
     "context": "周胜益 卸任县长，彭礼 接任代理县长（2026）",
     "overlap_org": "龙山县人民政府", "overlap_period": "2026-07"},
    {"person_a": 5, "person_b": 3, "type": "predecessor_successor",
     "context": "刘冬生(2019-2022书记) 卸任由时荣芬接任",
     "overlap_org": "中共龙山县委员会", "overlap_period": "2022-01"},
    {"person_a": 5, "person_b": 4, "type": "superior_subordinate",
     "context": "刘冬生曾任龙山县长（2016-2019），周胜益继任县长",
     "overlap_org": "龙山县人民政府", "overlap_period": "2019"},
    # 张-龙志勇 / 杨甜 同事
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "张兵(纪委书记)、龙志勇(县委领导) 2025-06 同场警示教育会，共事龙山县委",
     "overlap_org": "中共龙山县委员会", "overlap_period": "2025"},
    # 人大/政协领导与党政主官
    {"person_a": 11, "person_b": 1, "type": "overlap",
     "context": "吴光文(书记) 与周大钊(人大主任) 同届共治龙山",
     "overlap_org": "龙山县", "overlap_period": "2026"},
    {"person_a": 12, "person_b": 1, "type": "overlap",
     "context": "杨波(政协主席) 与吴光文 同届共治龙山",
     "overlap_org": "龙山县", "overlap_period": "2026"},
    # 吴光文 跨地级市调任 (岳阳→湘西)
    {"person_a": 1, "person_b": 5, "type": "promotion_chain",
     "context": "吴光文 由岳阳县长跨地级市调任龙山县委书记（岳阳→湘西跨市交流）",
     "overlap_org": "湖南省委/湘西州委", "overlap_period": "2026-04"},
    # 保靖籍(周胜益)网络
    {"person_a": 4, "person_b": 3, "type": "same_region",
     "context": "周胜益(龙山县长)为湖南保靖人，时荣芬(花垣人)同为湘西本地干部",
     "overlap_org": "湘西土家族苗族自治州", "overlap_period": "2022-2026"},
]

DB_PATH = str(SCRIPT_DIR / "龙山县_network.db")
GEXF_PATH = str(SCRIPT_DIR / "龙山县_network.gexf")

if __name__ == "__main__":
    slug = "龙山县"
    db_path = SCRIPT_DIR / f"{slug}_network.db"
    gexf_path = SCRIPT_DIR / f"{slug}_network.gexf"

    try:
        run_build(
            slug=slug,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=str(db_path),
            gexf_path=str(gexf_path),
            overwrite=True,
        )
        print(f"Runner API OK: {len(persons)} persons, {len(organizations)} orgs, "
              f"{len(positions)} positions, {len(relationships)} relationships")
    except Exception as e:
        print(f"runner API failed: {e}")
        print("Falling back to direct build...")
        os.makedirs(SCRIPT_DIR, exist_ok=True)
        conn = sqlite3.connect(str(db_path))
        conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '');
        CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '', level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '');
        CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '');
        CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '');
        """)
        for p in persons:
            conn.execute(
                "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                 p["education"], p["party_join"], p["work_start"], p["current_post"],
                 p["current_org"], p["source"]))
        for o in organizations:
            conn.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                         (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
        for pos in positions:
            conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                         (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
                          pos["end_date"], pos["rank"], pos["note"]))
        for r in relationships:
            conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                         (r["person_a"], r["person_b"], r["type"], r["context"],
                          r["overlap_org"], r["overlap_period"]))
        conn.commit()
        conn.close()
        print(f"SQLite DB: {db_path}")
        builder = GEXFBuilder(title=slug)
        for p in persons:
            builder.add_person(id=p["id"], name=p["name"], current_post=p["current_post"],
                               current_org=p["current_org"], gender=p.get("gender", ""),
                               ethnicity=p.get("ethnicity", ""), birth=p.get("birth", ""),
                               source=p.get("source", ""))
        for o in organizations:
            builder.add_organization(id=o["id"] + 100000, name=o["name"], org_type=o["type"],
                                     level=o["level"], location=o["location"])
        for r in relationships:
            builder.add_relationship(source=r["person_a"], target=r["person_b"], rel_type=r.get("type", ""),
                                     context=r.get("context", ""), overlap_org=r.get("overlap_org", ""),
                                     overlap_period=r.get("overlap_period", ""))
        builder.write(gexf_path)
        print(f"GEXF graph: {gexf_path}")

    print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print(f"Output: {db_path}, {gexf_path}")