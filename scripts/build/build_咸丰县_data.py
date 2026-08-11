#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 咸丰县 (Xianfeng County), 湖北省恩施州.

Task ID: hubei_咸丰县
Province: 湖北省
Parent city: 恩施土家族苗族自治州
Level: 县级
Targets: 县委书记 & 县长
Investigation date: 2026-08-11

Core confirmed leadership (as of 2026-08):
  - 县委书记 覃正炜: promoted from 县长 after 郭玲 left Nov 2025 (official + media)
  - 县委副书记、县长 郭亚妮: 代理县长 2025-11-28, elected 县长 2025-12 (official gov bio)
  - 县委常委、常务副县长 金韬 (2026-08), 县委常委、政法委书记 杨俊 (2026-03)
Government roster via 咸丰县政府 领导之窗 (zfld) —— current as of 2026-08-04.

Predecessor chain: 刘忠义→郑东来(2016-12, 后双开)→郭玲(2021-07, →州委统战部长)→覃正炜(2025-11).
县长 chain: 杨皓(2016-12)→覃正炜(2021-08)→郭亚妮(2025-11).
Cross-county: 王兵 (咸丰副县长/常委政法书记/常务副县长 2011-2019 → 州政府 → 鹤峰县长 → 来凤县委书记 2026-06).
Context: 恩施州委书记胡超文 2026-05-06 接受审查调查; 张忠军 2026-05-18 任州委书记。
Risk signal: 前县委书记郑东来 2023-04 双开（受贿罪、滥用职权罪移送起诉）。

Confidence notes:
  - 覃正炜/郭亚妮/金韬 履历 CONFIRMED (官方简历)
  - 政府班子其余成员职位 CONFIRMED (政府网领导之窗), 个人履历未获 -> open gaps
  - 杨俊 职务 CONFIRMED (恩施州检察院 2026-03 报道), 履历未获 -> open gap
  - 郭玲/郑东来/杨皓/王兵/邹炜 履历 CONFIRMED via 官方及权威媒体
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "咸丰县"
PROVINCE = "湖北省"
CITY = "恩施土家族苗族自治州"
AS_OF = "2026-08-11"
TASK_ID = "hubei_咸丰县"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────
persons = [
    # ── Current leadership ─────────────────────────────────────────
    {"id": 1, "name": "覃正炜", "gender": "男", "ethnicity": "土家族", "birth": "1981年10月", "birthplace": "湖北鹤峰",
     "education": "中南财经政法大学本科；湖北省委党校法学专业在职研究生", "party_join": "2004年12月", "work_start": "2003年7月",
     "current_post": "县委书记", "current_org": "中共咸丰县委员会",
     "source": "百度百科覃正炜词条; 咸丰县政府门户; 武汉市人民政府网2025-12-14",
     "notes": "2025年11月起任县委书记、县人武部党委第一书记（2025-12-17宣布）；此前2021-08~2025-11任咸丰县长；更早任鹤峰县委副书记、团州委书记、建始县副县长等。"},
    {"id": 2, "name": "郭亚妮", "gender": "女", "ethnicity": "苗族", "birth": "1983年2月", "birthplace": "湖北宣恩",
     "education": "大学学历，管理学学士（湖北民族学院）", "party_join": "2007年6月", "work_start": "2005年7月",
     "current_post": "县委副书记、县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（官方简历）; 凤凰网湖北2025-12-01; 恩施州检察院2026-03",
     "notes": "2025-11-28任代理县长，2025-12经县十九届人大五次会议当选县长；此前任恩施州信访局局长、社会工作部副部长；早年历任共青团巴东县委书记、巴东沿渡河镇长、恩施州妇联副主席、恩施市委常委/宣传部长/市委副书记、统战部长。"},
    {"id": 3, "name": "金韬", "gender": "男", "ethnicity": "汉族", "birth": "1975年1月", "birthplace": "浙江临海",
     "education": "大学文化，华中农业大学林学专业", "party_join": "2001年6月", "work_start": "1992年8月",
     "current_post": "县委常委、常务副县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗·金韬页（2026-07-22）",
     "notes": "2021-11任副县长，2025-04任县委常委、县委办主任，2026-08任常务副县长。"},
    {"id": 4, "name": "杨俊", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、县委政法委书记", "current_org": "中共咸丰县委员会",
     "source": "湖北省咸丰县人民检察院2026-03-16报道；恩施州检察院调研咸丰",
     "notes": "2026-03以县委常委、政法委书记身份参加恩施州检察院调研咸丰活动。出生、履历未公开。"},
    # ── 政府班子（官方领导之窗, 2026-08） ─────────────────────────
    {"id": 5, "name": "姜玉桂", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2024-01-12）",
     "notes": "2024-01分管政务、市场监管等（角色/分工见领导之窗）；简历未公开。"},
    {"id": 6, "name": "唐红珍", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2021-12-22）；中国民主建国会湖北省委员会2025-10-16",
     "notes": "2021-12起任副县长；同时任民建恩施州委副主委（2025-10-16在郭玲走访民主党派座谈会上出席）——党外干部（民建）身份待官方确认。"},
    {"id": 7, "name": "申金桥", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2021-12-22）",
     "notes": "简历未公开。"},
    {"id": 8, "name": "王海涛", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2026-08-04）",
     "notes": "2026-08任副县长；简历未公开。"},
    {"id": 9, "name": "胡志", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2025-10-09）",
     "notes": "简历未公开。"},
    {"id": 10, "name": "钱洁", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2025-12-03）",
     "notes": "简历未公开。"},
    {"id": 11, "name": "何祥", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府党组成员", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2025-11-19）",
     "notes": ""},
    {"id": 12, "name": "袁明江", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府党组成员", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2025-11-13）；国硒中心专家工作站2023-08",
     "notes": "2023-08公开身份为咸丰县人民政府党组成员、副县长；2025-11政府网显示县政府党组成员。"},
    {"id": 13, "name": "申艳", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府党组成员", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2025-11-13）",
     "notes": ""},
    {"id": 14, "name": "赵中美", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府党组成员", "current_org": "咸丰县人民政府",
     "source": "咸丰县人民政府门户·政府领导之窗（2025-11-13）",
     "notes": ""},
    # ── 前任领导（去向/落马/牺牲）───────────────────────────────
    {"id": 15, "name": "郭玲", "gender": "女", "ethnicity": "土家族", "birth": "1979年2月", "birthplace": "湖北来凤",
     "education": "大学、在职公共管理硕士（浙江大学在职研究生）", "party_join": "1999年5月", "work_start": "1999年9月",
     "current_post": "恩施州委常委、州委统战部部长", "current_org": "中共恩施州委统战部",
     "source": "澎湃新闻2025-10; 京报网2025-10-14; 恩施州委统战部官网; 新京报2025-09-22",
     "notes": "前任咸丰县委书记（2021-07~2025-10）；2025-09任前公示拟任市州党委常委，2025-10任恩施州委常委、统战部部长。曾任巴东县委副书记、县长（2016-12~2021-07）。"},
    {"id": 16, "name": "郑东来", "gender": "男", "ethnicity": "苗族", "birth": "1966年10月", "birthplace": "湖北宣恩",
     "education": "大学学历（中央党校国民经济管理专业）", "party_join": "1998年3月", "work_start": "1986年7月",
     "current_post": "（前任咸丰县委书记，已落马）", "current_org": "",
     "source": "湖北省纪委监委通报（中央纪委国家监委网站2023-12-18转载）; 中国经济网2016-12-05; 咸丰县法院网站2016-12-20",
     "notes": "咸丰县委书记2016-12~2021-07；2021-08任州政府党组成员，2021-11任州发改委主任；2022-12免职；2023-04被开除党籍、开除公职（受贿、滥用职权），2023-12因长江大保护虚假整改被中央纪委通报。"},
    {"id": 17, "name": "杨皓", "gender": "男", "ethnicity": "苗族", "birth": "1965年11月", "birthplace": "湖北利川",
     "education": "大学学历，湖北大学汉语言文学专业", "party_join": "1992年9月", "work_start": "1987年1月",
     "current_post": "恩施州政协党组成员、秘书长", "current_org": "恩施州政协",
     "source": "咸丰县新闻网2016-12-20; 长江网恩施日报2023-07-24",
     "notes": "前任咸丰县长（2016-12~2021）；曾任鹤峰副县长/常务副县长（2006-11~2015）、恩施州编办主任（2015-01）；后任恩施州政协党组成员、秘书长（2023-07报道确认）。"},
    {"id": 18, "name": "邹炜", "gender": "男", "ethnicity": "土家族", "birth": "1979年12月", "birthplace": "湖北巴东",
     "education": "省委党校研究生", "party_join": "2003年6月", "work_start": "2002年7月",
     "current_post": "（原咸丰县委副书记，2018年因公殉职）", "current_org": "中共咸丰县委员会",
     "source": "澎湃新闻2018-12-24; 湖北文明网2020-01; 咸丰县新闻网",
     "notes": "2016-12~2018-12任咸丰县委副书记，分管脱贫攻坚；2018-12-10进入拟任鹤峰县县长人选公示期；2018-12-18在前往忠堡镇检查脱贫攻坚途因交通事故殉职，时年39岁；曾获'感动恩施'2018-2019年度人物；曾任团州委副书记、恩施市委常委/宣传部长/统战部长、鹤峰县委常委/组织部长。"},
    {"id": 19, "name": "王兵", "gender": "男", "ethnicity": "土家族", "birth": "1978年3月", "birthplace": "湖北恩施",
     "education": "大学本科学历", "party_join": "2001年6月", "work_start": "1999年12月",
     "current_post": "来凤县委书记", "current_org": "中共来凤县委员会",
     "source": "今日头条/云上来凤2026-06-26; 恩施州8县市新一届党委班子新闻",
     "notes": "跨县干部：2011-10起在咸丰任职8年——副县长(2011-10)→常委/政法委书记(2014-12)→常务副县长(2016-12)→州政府机关党组成员、副秘书长→鹤峰县委副书记、代理县长(2021-08)→鹤峰县长(2021-11)→来凤县委书记(2026-06-25报道'云上来凤')。在咸丰期间与郑东来(书记)、杨皓(县长)搭档。"},
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共咸丰县委员会", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "湖北省恩施州咸丰县"},
    {"id": 2, "name": "咸丰县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施州咸丰县"},
    {"id": 3, "name": "咸丰县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "咸丰县", "location": "湖北省恩施州咸丰县"},
    {"id": 4, "name": "咸丰县政协", "type": "政协", "level": "县级", "parent": "咸丰县", "location": "湖北省恩施州咸丰县"},
    {"id": 5, "name": "中共恩施州委", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "湖北省恩施州"},
    {"id": 6, "name": "恩施州人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "湖北省恩施州"},
    {"id": 7, "name": "恩施州人大常委会", "type": "人大", "level": "地级市", "parent": "湖北省人大常委会", "location": "湖北省恩施州"},
    {"id": 8, "name": "恩施州政协", "type": "政协", "level": "地级市", "parent": "湖北省政协", "location": "湖北省恩施州"},
    {"id": 9, "name": "中共恩施州委统战部", "type": "党委", "level": "地级市", "parent": "中共恩施州委", "location": "湖北省恩施州"},
    {"id": 10, "name": "中共恩施州委社会工作部", "type": "党委", "level": "地级市", "parent": "中共恩施州委", "location": "湖北省恩施州"},
    {"id": 11, "name": "恩施州信访局", "type": "政府", "level": "地级市", "parent": "恩施州人民政府", "location": "湖北省恩施州"},
    {"id": 12, "name": "中共来凤县委员会", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "湖北省恩施州来凤县"},
    {"id": 13, "name": "中共鹤峰县委员会", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "湖北省恩施州鹤峰县"},
    {"id": 14, "name": "鹤峰县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施州鹤峰县"},
    {"id": 15, "name": "中共巴东县委员会", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "湖北省恩施州巴东县"},
    {"id": 16, "name": "巴东县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施州巴东县"},
    {"id": 17, "name": "中共恩施市委员会", "type": "党委", "level": "县级市", "parent": "中共恩施州委", "location": "湖北省恩施州恩施市"},
    {"id": 18, "name": "恩施市人民政府", "type": "政府", "level": "县级市", "parent": "恩施州人民政府", "location": "湖北省恩施州恩施市"},
    {"id": 19, "name": "共青团恩施州委员会", "type": "群团", "level": "地级市", "parent": "中共恩施州委", "location": "湖北省恩施州"},
    {"id": 20, "name": "建始县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施州建始县"},
    {"id": 21, "name": "中共建始县委员会", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "湖北省恩施州建始县"},
    {"id": 22, "name": "恩施州发展和改革委员会", "type": "政府", "level": "地级市", "parent": "恩施州人民政府", "location": "湖北省恩施州"},
    {"id": 23, "name": "恩施州妇联", "type": "群团", "level": "地级市", "parent": "中共恩施州委", "location": "湖北省恩施州"},
]

# ── Positions ──────────────────────────────────────────────────────
positions = [
    # 覃正炜 (1)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2025-11", "end": "present", "rank": "正处级", "note": "县人武部党委第一书记（2025-12-17宣布）"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长", "start": "2021-11", "end": "2025-11", "rank": "正处级", "note": "2021-08起代理县长"},
    {"person_id": 1, "org_id": 13, "title": "县委副书记、县委党校校长", "start": "2019-03", "end": "2021-08", "rank": "副处级/一级调研员", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "共青团恩施州委书记", "start": "2016-01", "end": "2019-02", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 21, "title": "县委常委、统战部部长", "start": "2014-10", "end": "2016-01", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 20, "title": "副县长", "start": "2011-10", "end": "2014-10", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "共青团恩施州委副书记", "start": "2010-11", "end": "2011-10", "rank": "副处级", "note": ""},
    # 郭亚妮 (2)
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2025-12", "end": "present", "rank": "正处级", "note": "2025-12县十九届人大五次会议当选"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2025-11", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "副县长、代理县长", "start": "2025-11", "end": "2025-12", "rank": "正处级", "note": "2025-11-28十九届人大常委会第二十九次会议决定"},
    {"person_id": 2, "org_id": 10, "title": "州委社会工作部副部长", "start": "2024-07", "end": "2025-11", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "州信访局党组书记、局长", "start": "2023-07", "end": "2025-11", "rank": "正处级", "note": "2024-07起兼任州委社会工作部副部长"},
    {"person_id": 2, "org_id": 17, "title": "市委常委、市委宣传部部长", "start": "2016-09", "end": "2019", "rank": "副处级", "note": "2019年前后转任市委副书记"},
    {"person_id": 2, "org_id": 17, "title": "市委副书记（兼统战部部长）", "start": "2019", "end": "2023-07", "rank": "副处级", "note": "2023-05以市委副书记、统战部部长身份出席公开活动"},
    {"person_id": 2, "org_id": 23, "title": "州妇联党组成员、副主席", "start": "2012-10", "end": "2016-08", "rank": "副处级", "note": ""},
    # 金韬 (3)
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "2026-08", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委常委、县委办公室主任", "start": "2025-04", "end": "2026-08", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长", "start": "2021-11", "end": "2025-04", "rank": "副处级", "note": ""},
    # 杨俊 (4)
    {"person_id": 4, "org_id": 1, "title": "县委常委、县委政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "2026-03已履职"},
    # 政府班子
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "2024-01", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "2021-12", "end": "present", "rank": "副处级", "note": "民建恩施州委副主委（党外干部）"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "2021-12", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "2026-08", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "2025-10", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "2025-12", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县政府党组成员", "start": "2025-11", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "县政府党组成员（曾任副县长）", "start": "2025-11", "end": "present", "rank": "副处级", "note": "2023-08以党组成员、副县长身份公开出席活动"},
    {"person_id": 13, "org_id": 2, "title": "县政府党组成员", "start": "2025-11", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "县政府党组成员", "start": "2025-11", "end": "present", "rank": "副处级", "note": ""},
    # 郭玲 (15)
    {"person_id": 15, "org_id": 9, "title": "恩施州委常委、州委统战部部长", "start": "2025-10", "end": "present", "rank": "副厅级", "note": "2025-09任前公示，拟任市州党委常委"},
    {"person_id": 15, "org_id": 1, "title": "县委书记", "start": "2021-07", "end": "2025-10", "rank": "正处级", "note": "二级巡视员"},
    {"person_id": 15, "org_id": 16, "title": "巴东县委副书记、县长", "start": "2016-12", "end": "2021-07", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 19, "title": "共青团恩施州委书记", "start": "2012-05", "end": "2016-12", "rank": "正处级", "note": "任职起始时间待核"},
    {"person_id": 15, "org_id": 20, "title": "建始县副县长", "start": "2010-02", "end": "2012-05", "rank": "副处级", "note": "任职起始时间待核"},
    # 郑东来 (16)
    {"person_id": 16, "org_id": 22, "title": "州发展和改革委员会主任", "start": "2021-11", "end": "2022-12", "rank": "正处级", "note": "2021-08任州政府党组成员"},
    {"person_id": 16, "org_id": 1, "title": "县委书记", "start": "2016-12", "end": "2021-07", "rank": "正处级", "note": "同时兼任县人大常委会主任；2023-04双开"},
    {"person_id": 16, "org_id": 2, "title": "县人民政府县长", "start": "2015-04", "end": "2016-12", "rank": "正处级", "note": "2015-12转正"},
    {"person_id": 16, "org_id": 6, "title": "州商务（招商）局局长", "start": "2011-12", "end": "2015-04", "rank": "正处级", "note": ""},
    # 杨皓 (17)
    {"person_id": 17, "org_id": 8, "title": "州政协党组成员、秘书长", "start": "2021-10", "end": "present", "rank": "正处级", "note": "2023-07报道确认；起始时间待核"},
    {"person_id": 17, "org_id": 2, "title": "县长", "start": "2016-12", "end": "2021-07", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "县委副书记", "start": "2016-12", "end": "2021-07", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 5, "title": "恩施州编委会办公室主任", "start": "2015-01", "end": "2016-12", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 13, "title": "鹤峰县委常委、常务副县长", "start": "2011-11", "end": "2015-01", "rank": "副处级", "note": "2006-11起任鹤峰副县长"},
    # 邹炜 (18)
    {"person_id": 18, "org_id": 1, "title": "县委副书记", "start": "2016-12", "end": "2018-12", "rank": "副处级", "note": "分管脱贫攻坚；2018-12-18因公殉职"},
    {"person_id": 18, "org_id": 13, "title": "鹤峰县委常委、组织部部长", "start": "2014-10", "end": "2016-12", "rank": "副处级", "note": "时间待核"},
    {"person_id": 18, "org_id": 17, "title": "恩施市委常委、宣传部部长、统战部部长", "start": "2010-05", "end": "2014-10", "rank": "副处级", "note": "时间待核"},
    {"person_id": 18, "org_id": 19, "title": "共青团恩施州委副书记", "start": "2006-10", "end": "2010-05", "rank": "副处级", "note": "时间待核"},
    # 王兵 (19)
    {"person_id": 19, "org_id": 12, "title": "来凤县委书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 14, "title": "鹤峰县委副书记、县长", "start": "2021-11", "end": "2026-06", "rank": "正处级", "note": "2021-08起代理县长"},
    {"person_id": 19, "org_id": 6, "title": "州政府机关党组成员、副秘书长", "start": "2019", "end": "2021-08", "rank": "正处级", "note": "时间段待核"},
    {"person_id": 19, "org_id": 2, "title": "常务副县长", "start": "2016-12", "end": "2019", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 1, "title": "县委常委、政法委书记", "start": "2014-12", "end": "2016-12", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "副县长", "start": "2011-10", "end": "2014-12", "rank": "副处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────
relationships = [
    # 现任党政正职
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记与县长搭档主持县委、县政府全面工作（2025-11郭亚妮到任后组成班子）",
     "overlap_org": "咸丰县", "overlap_period": "2025-11至今", "confidence": "confirmed"},
    # 书记交接
    {"person_a": 15, "person_b": 1, "type": "前后任",
     "context": "郭玲离任咸丰县委书记（2025-10）后由覃正炜接任",
     "overlap_org": "中共咸丰县委员会", "overlap_period": "2025", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 2, "type": "县长交棒",
     "context": "覃正炜卸任县长升任县委书记，郭亚妮接任代理县长并当选县长",
     "overlap_org": "咸丰县人民政府", "overlap_period": "2025-11", "confidence": "confirmed"},
    # 现任班子内部
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "金韬任县委办主任（2025-04）期间及调任常务副县长（2026-08）后均为县委书记直接下属",
     "overlap_org": "咸丰县人民政府", "overlap_period": "2025-04至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "县长与常务副县长共同主持政府常务工作",
     "overlap_org": "咸丰县人民政府", "overlap_period": "2026-08至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "县委书记与县委政法委书记（2026-03一同参加州检察院调研）",
     "overlap_org": "中共咸丰县委员会", "overlap_period": "2025-2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "县长与分管副职；唐红珍为县政府仅有的民主党派（民建）干部",
     "overlap_org": "咸丰县人民政府", "overlap_period": "2025-12至今", "confidence": "confirmed"},
    # 前任链条
    {"person_a": 16, "person_b": 15, "type": "前后任",
     "context": "郑东来2021-07离任后由郭玲接任咸丰县委书记",
     "overlap_org": "中共咸丰县委员会", "overlap_period": "2021-07", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 17, "type": "党政搭档",
     "context": "书记与县长搭档主持全县工作（2016-2021）",
     "overlap_org": "咸丰县", "overlap_period": "2016-12至2021-07", "confidence": "confirmed"},
    {"person_a": 17, "person_b": 1, "type": "前后任",
     "context": "杨皓离任咸丰县长后由覃正炜2021-08接任（先代理）",
     "overlap_org": "咸丰县人民政府", "overlap_period": "2021", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 18, "type": "上下级",
     "context": "郑东来任书记期间邹炜任县委副书记分管脱贫攻坚，邹2018-12-18扶贫途中殉职",
     "overlap_org": "中共咸丰县委员会", "overlap_period": "2016-12至2018-12", "confidence": "confirmed"},
    {"person_a": 17, "person_b": 18, "type": "同僚",
     "context": "县长与县委副书记会同在县委班子（2016-12至2018-12）",
     "overlap_org": "咸丰县", "overlap_period": "2016-12至2018-12", "confidence": "confirmed"},
    # 跨县流动 · 王兵
    {"person_a": 16, "person_b": 19, "type": "上下级",
     "context": "王兵任咸丰常务副县长期间为郑东来书记的直接下级（2016-12~2019）",
     "overlap_org": "咸丰县", "overlap_period": "2016-12至~2019", "confidence": "confirmed"},
    {"person_a": 17, "person_b": 19, "type": "上下级",
     "context": "王兵任常务副县长期间为杨皓县长的直接下级",
     "overlap_org": "咸丰县人民政府", "overlap_period": "2016-12至~2019", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 19, "type": "跨县同体系",
     "context": "覃正炜2021接任咸丰县长时王兵已离任，但二人均沿'咸丰-鹤峰-来凤'干部流动通道发展（覃正炜曾任鹤峰县委副书记2019-2021）",
     "overlap_org": "恩施州", "overlap_period": "2019-2026", "confidence": "plausible"},
    # 统战同场（郭玲-唐红珍）
    {"person_a": 15, "person_b": 6, "type": "同场合",
     "context": "郭玲任州委统战部长后走访民建恩施州委，副主委唐红珍（咸丰副县长）参加座谈",
     "overlap_org": "恩施州委统战部", "overlap_period": "2025-10-16", "confidence": "confirmed"},
]

# ── 来源登记 ──────────────────────────────────────────────────────
SOURCES = [
    {"id": "S001", "title": "咸丰县人民政府·政府领导之窗（郭亚妮）", "url": "http://www.xianfeng.gov.cn/xxgk/gkml/zfld/202512/t20251204_1760792.shtml",
     "publisher": "咸丰县人民政府办公室", "published_at": "2025-12-04", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "县长郭亚妮官方简历（含州信访局/社会工作部履历）及当前政府班子名单"},
    {"id": "S002", "title": "咸丰县人民政府·政府领导之窗（金韬）", "url": "http://www.xianfeng.gov.cn/xxgk/gkml/zfld/202607/t20260722_1821226.shtml",
     "publisher": "咸丰县人民政府办公室", "published_at": "2026-07-22", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "金韬简历：2021-11副县长、2025-04县委办主任、2026-08常务副县长"},
    {"id": "S003", "title": "百度百科·覃正炜", "url": "https://baike.baidu.com/item/覃正炜/9905086",
     "publisher": "百度百科", "published_at": "2026", "accessed_at": AS_OF,
     "source_type": "encyclopedia", "reliability": "medium", "notes": "完整履历（利川/建始/团州委/鹤峰/咸丰）及县人武部第一书记任命（2025-12-17）"},
    {"id": "S004", "title": "郭亚妮任咸丰县人民政府副县长、代理县长", "url": "https://hb.china.com/news/20003178/20251201/25983494.html",
     "publisher": "凤凰网湖北/中华网", "published_at": "2025-12-01", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "medium", "notes": "2025-11-28县十九届人大常委会第二十九次会议任命"},
    {"id": "S005", "title": "湖北咸丰县委书记郭玲升任恩施州委常委、统战部部长", "url": "https://www.thepaper.cn/newsDetail_forward_31779204",
     "publisher": "澎湃新闻", "published_at": "2025-10", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high", "notes": "郭玲完整履历（史志办→组织部→接待处→建始→团州委→巴东→咸丰→州统战部）"},
    {"id": "S006", "title": "县委书记郭玲，拟提拔", "url": "https://www.bjnews.com.cn/detail/1758517616129299.html",
     "publisher": "新京报", "published_at": "2025-09-22", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high", "notes": "任前公示：郭玲，女，土家族，1979年2月生，咸丰县委书记、二级巡视员，拟任市州党委常委"},
    {"id": "S007", "title": "恩施州检察院调研组到咸丰调研指导工作", "url": "https://xf.es.hbjc.gov.cn/jcxw_72705/tt_72706/202603/t20260316_1881821.shtml",
     "publisher": "咸丰县人民检察院", "published_at": "2026-03-16", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "确认覃正炜=县委书记、郭亚妮=县委副书记/县长、杨俊=县委常委/政法委书记"},
    {"id": "S008", "title": "盛阅春率队赴恩施州咸丰县开展结对帮扶工作", "url": "https://www.wuhan.gov.cn/sy/whyw/202512/t20251214_2694777.shtml",
     "publisher": "武汉市人民政府", "published_at": "2025-12-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "覃正炜以咸丰县委书记、郭亚妮以代理县长身份参加"},
    {"id": "S009", "title": "咸丰县新一届县委领导班子产生（2016十四届）", "url": "https://xfxfy.hbfy.gov.cn/docmanage/viewdoc?docid=759ba48e-d6b3-4923-baf9-bb655aaa9e3f",
     "publisher": "咸丰县人民法院网转载", "published_at": "2016-12-20", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "medium", "notes": "2016年14届县委班子：郑东来/杨皓/邹炜及王兵等8常委的完整简历"},
    {"id": "S010", "title": "搞虚假整改，湖北一官员再被点名通报", "url": "https://s.cyol.com/articles/2023-12/18/content_v69Rmzc4.html",
     "publisher": "中国青年报/中央纪委国家监委网站", "published_at": "2023-12-18", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "郑东来2023-04双开通报、2023-12长江保护虚假整改通报"},
    {"id": "S011", "title": "恩施日报刊文悼念在脱贫攻坚中牺牲的基层干部邹炜、李勇", "url": "https://www.thepaper.cn/newsDetail_forward_2769230",
     "publisher": "澎湃新闻转载恩施日报", "published_at": "2018-12-24", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high", "notes": "邹炜2018-12-18殉职；拟任鹤峰县长公示（2018-12-10）"},
    {"id": "S012", "title": "王兵任恩施州来凤县委书记", "url": "https://www.toutiao.com/article/7655682496771785222/",
     "publisher": "今日头条/云上来凤", "published_at": "2026-06-26", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "medium", "notes": "王兵完整履历：咸丰10年（2011-10起副县长/常委/常务副县长）→州政府副秘书长→鹤峰县长→来凤书记"},
    {"id": "S013", "title": "恩施州政协机关开展主题党日活动", "url": "http://news.cjn.cn/hbpd_19912/yw_19915/202307/t4633398.htm",
     "publisher": "长江网/恩施日报", "published_at": "2023-07-24", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "medium", "notes": "杨皓以州政协党组成员、秘书长身份参加活动"},
    {"id": "S014", "title": "咸丰县2024年政府工作报告", "url": "https://www.quyushuju.com/forum.php?mod=viewthread&tid=78018",
     "publisher": "咸丰县人民政府", "published_at": "2024-01", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "medium", "notes": "2023年GDP 122亿元；唐崖茶/富硒/文旅数据（覃正炜作报告）"},
    {"id": "S015", "title": "湖北恩施开展'铁腕治旅'大讨论", "url": "https://www.thepaper.cn/newsDetail_forward_33543893",
     "publisher": "澎湃新闻", "published_at": "2026-07", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "medium", "notes": "郭亚妮以咸丰县委副书记、县长身份介绍'铁腕治旅'安排（2026-07）"},
    {"id": "S016", "title": "鄂地重燃'烟火气'——咸丰县农特产品亮相武汉茅庙集庙会", "url": "https://gxs.wuhan.gov.cn/gxxw/qsgz/202402/t20240206_2358068.shtml",
     "publisher": "武汉市供销合作总社", "published_at": "2024-02-06", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "medium", "notes": "覃正炜以咸丰县长身份（2024-02）参加东西湖结对帮扶活动"},
    {"id": "S017", "title": "郭亚妮（中文百科全书人物）", "url": "https://www.newton.com.tw/wiki/郭亚妮/2950881",
     "publisher": "newton.com.tw", "published_at": "2018", "accessed_at": AS_OF,
     "source_type": "database", "reliability": "low", "notes": "郭亚妮2016-2019恩施市任职履历（团巴东书记→沿渡河镇长→州妇联→恩施市）"},
    {"id": "S018", "title": "2025年12月27日 咸丰县十九届人大五次会议投票表决民生实事", "url": "https://www.news.cn/politics/20260311/0b78600df3e24b28a6056d0905035f44/c.html",
     "publisher": "新华社", "published_at": "2026-03-11", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "县十九届人大五次会议（2025-12-27）——郭亚妮当选县长的届次"},
    {"id": "S019", "title": "中共恩施州委常委、统战部部长郭玲走访调研各民主党派和工商联", "url": "https://hbmj.gov.cn/a/18425.html",
     "publisher": "中国民主建国会湖北省委员会", "published_at": "2025-10-16", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "medium", "notes": "唐红珍以民建恩施州委副主委身份参加座谈"},
]


# ── Person JSON 生成 ───────────────────────────────────────────────

def build_profile_json(pid: int, job: str) -> dict:
    p = next(x for x in persons if x["id"] == pid)
    name = p["name"]
    timeline = []
    for pos in positions:
        if pos["person_id"] == pid:
            org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
            timeline.append({
                "start": pos["start"], "end": pos["end"], "org": org_name, "title": pos["title"],
                "level": "", "location": PROVINCE + CITY, "system": "party",
                "rank": pos["rank"], "is_key_promotion": False, "notes": pos.get("note", ""),
                "confidence": "confirmed"
                if pid in (1, 2, 3) or pos.get("rank") in ("正处级",)
                else "plausible",
                "source_ids": ["S001", "S002", "S003"] if pid in (1, 2, 3) else ["S009"],
            })
    professional = {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
    }
    profile_by_name = {
        "覃正炜": {
            "primary_specializations": ["县域经济", "共青团/青年工作", "基层治理"],
            "career_pattern": "cross_county_rotation",
            "systems_experience": ["共青团", "政府", "党务"],
            "geographic_pattern": ["利川", "建始", "恩施州", "鹤峰", "咸丰"],
            "promotion_velocity": {"summary": "1981年生，2025年44岁时升任县委书记；共青团系统起家，政企/政府双线",
                                   "notable_fast_promotions": ["2016-01 任团恩施州委书记（34岁正处）"]},
        },
        "郭亚妮": {
            "primary_specializations": ["宣传/意识形态", "统战", "信访维稳"],
            "career_pattern": "cross_county_rotation",
            "systems_experience": ["共青团", "妇联", "宣传", "统战", "信访"],
            "geographic_pattern": ["巴东", "恩施市", "恩施州", "咸丰"],
            "promotion_velocity": {"summary": "1983年生，2025年42岁升任正处级县长；州信访局长→县长为省级平级交流模式", "notable_fast_promotions": []},
        },
        "金韬": {
            "primary_specializations": ["财政税务/国资", "办公室系统"],
            "career_pattern": "local_ladder",
            "systems_experience": ["政府", "县委办"],
            "geographic_pattern": ["恩施州", "咸丰"],
            "promotion_velocity": {"summary": "2021-11至2026-08五年内由副县长、县委办主任到常务副县长", "notable_fast_promotions": []},
        },
        "郭玲": {
            "primary_specializations": ["党委部门", "县域治理", "统战"],
            "career_pattern": "organization_track",
            "systems_experience": ["党委机关", "政府", "共青团", "统战"],
            "geographic_pattern": ["建始", "巴东", "咸丰", "恩施州"],
            "promotion_velocity": {"summary": "1979年生，县-州两级主官女性干部代表；2025-10升副厅级州委常委", "notable_fast_promotions": []},
        },
    }
    professional_profile = profile_by_name.get(name, {})
    if not professional_profile:
        professional_profile = {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [SLUG],
            "promotion_velocity": {"summary": "简历未公开/待核", "notable_fast_promotions": []},
        }

    risks = [
        {"type": "disciplinary_action",
         "description": "前任咸丰县委书记郑东来因涉嫌受贿罪、滥用职权罪于2023-04被开除党籍、开除公职，移送检察院；2023-12因长江大保护整改虚假报送被中央纪委通报（涉该县忠建河大鲵保护区龙坪电站）",
         "date": "2023-04/2023-12", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    if name == "郭玲":
        risks.append({"type": "none_found",
                      "description": "公开渠道未发现郭玲个人负面纪律信号（2026-08检索）",
                      "date": AS_OF, "confidence": "unverified", "source_ids": []})
    new_id = f"xianfeng_{pid}_{name}"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": job,
                                "task_id": TASK_ID, "time_focus": "2021-2026"},
        "identity": {
            "person_id": new_id, "name": name, "aliases": [], "gender": p["gender"],
            "ethnicity": p["ethnicity"], "birth": p["birth"], "birthplace": p["birthplace"],
            "native_place": p["birthplace"] or "",
            "education": [{"period": "", "institution": p.get("education", ""), "major": "",
                           "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": p["party_join"], "work_start": p["work_start"],
            "dedupe_keys": {"name_birth": f"{name}_{p['birth']}",
                            "name_birthplace": f"{name}_{p['birthplace']}",
                            "official_profile_url": ""},
        },
        "current_status": {"current_post": p["current_post"], "current_org": p["current_org"],
                           "administrative_rank": "正处级" if pid in (1, 2) else ("副处级" if pid == 3 else ""),
                           "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S007", "S008"]},
        "career_timeline": timeline,
        "organizations": [{"org": o["name"], "type": o["type"], "level": o["level"], "location": o["location"]}
                          for o in organizations
                          if o["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == pid}],
        "relationships": [
            {
                "person": next(
                    (x["name"] for x in persons if x["id"] == (r["person_b"] if r["person_a"] == pid else r["person_a"])),
                    "",
                ),
                "person_id": "",
                "relationship_type": r["type"], "strength": "strong" if r.get("confidence") == "confirmed" else "medium",
                "evidence": r.get("context", ""), "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""), "direction": "undirected",
                "confidence": r.get("confidence", "unverified"), "source_ids": [],
            }
            for r in relationships if pid in (r["person_a"], r["person_b"])
        ],
        "governance_record": [
            {"period": "2023", "domain": "economic_development",
             "achievement_or_event": "全县实现地区生产总值122亿元、增长6.5%；规模以上工业增加值增长12%；引进浙江新安化工（皇恩烨新材料）、中茶湖北落户；法国电力新能源项目签约",
             "role_in_event": "时任县长覃正炜作县政府工作报告并主抓", "measurable_outcome": "GDP 122亿元/2023",
             "location": "咸丰县", "confidence": "confirmed", "source_ids": ["S014"]},
            {"period": "2023", "domain": "industry",
             "achievement_or_event": "生产干茶1.2万吨、产值破20亿元；获评全国2023年度重点产茶县域；唐崖茶获上海进博会金奖；'咸丰富硒白茶'入选全国'三茶'统筹案例",
             "role_in_org": "县政府主导产业培育", "measurable_outcome": "产值20亿元",
             "location": "咸丰县", "confidence": "confirmed", "source_ids": ["S014"]},
            {"period": "2026", "domain": "other",
             "achievement_or_event": "部署'铁腕治旅'专项行动：协调整合文旅/市监/公安/交通等执法力量（郭亚妮分抓）",
             "role_in_event": "县委副书记、县长郭亚妮代表咸丰发声", "measurable_outcome": "当年立案查办涉旅案件16起、通报2起",
             "location": "咸丰县", "confidence": "confirmed", "source_ids": ["S015"]},
        ],
        "professional_profile": professional_profile,
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented",
                 "evidence": "覃正炜2026-07赴高乐山镇调研强调'凝聚合力聚焦重点'；郭亚妮八一走访慰问；郑东来时代赴华中师大支教团慰问等",
                 "confidence": "plausible", "source_ids": []},
            ],
            "speech_themes": ["脱贫成果巩固", "富硒产业", "文化旅游（唐崖土司城）", "乡村振兴"],
            "management_signals": ["项目化指挥部署（县规划委员会/指挥部体制）"],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": risks,
        "source_register": SOURCES,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "complete" if pid in (1, 2, 3, 15, 16, 17, 18, 19) else "thin",
            "relationship_confidence": "high" if pid in (1, 2) else "medium",
            "biggest_gap": (
                "覃正炜任县委书记（2025-11）前的完整履历已获，但2026年县委班子名单（组织/纪检/宣传/统战部长）未获"
                if pid == 1 else
                "郭亚妮2019-2023在恩施市的市委副书记职务起始时间与细节" if pid == 2
                else f"{name}早年任职/简历细节"),
        },
        "open_questions": [
            {"priority": "high", "question": "2026年咸丰县委常委班子完整名单（组织部长/纪委书记/宣传部长/统战部长/县委办主任候任）",
             "why_it_matters": "班子网络完整性", "suggested_queries": ["咸丰县委常委 分工 2026", "咸丰县委 领导之窗"], "last_attempted": AS_OF},
            {"priority": "high", "question": "现任县人大常委会主任、县政协主席姓名",
             "why_it_matters": "四大班子完整性", "suggested_queries": ["咸丰县人大 主任 2026", "咸丰县政协 主席"], "last_attempted": AS_OF},
            {"priority": "medium", "question": f"{name} 详细任职起始时间（部分职位）" if pid not in (1, 2, 3) else "2019-2023年间任恩施市委副书记的准确任职时间",
             "why_it_matters": "时间线精度", "suggested_queries": [], "last_attempted": AS_OF},
        ],
    }


PERSON_JSONS = [
    ("shuji", "县委书记", 1),
    ("xianzhang", "县长", 2),
    ("changwu", "常务副县长", 3),
    ("qianrenshuji", "前任县委书记", 15),
    ("qianxianzhang", "前任县长", 17),
    ("qianxianshuji_luoma", "原县委书记", 16),
]


def write_person_json(dest_dir: Path) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for _key, job, pid in PERSON_JSONS:
        profile = build_profile_json(pid, job)
        fn = f"{TODAY}-{PROVINCE}-{CITY}-{job}-{profile['identity']['name']}.json"
        fp = dest_dir / fn
        fp.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        out.append(fp)
    return out


def main() -> None:
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
    jsons = write_person_json(HERE)
    print(f"DB:    {DB_PATH}")
    print(f"GEXF:  {GEXF_PATH}")
    for fp in jsons:
        print(f"JSON:  {fp}")
    print(f"persons: {len(persons)}, orgs: {len(organizations)}, "
          f"positions: {len(positions)}, relationships: {len(relationships)}")


if __name__ == "__main__":
    main()