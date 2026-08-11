#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 延吉市 (Yanji), 吉林省·延边朝鲜族自治州.

Task ID: jilin_延吉市 | Level: 县级市（州首府） | Targets: 市委书记 & 市长 | Date: 2026-08-11

Research summary (2026-08-11):
  现任市委书记=王吉宝（州委常委兼，2025-01履新，此前任安图县委书记）
  现任市委副书记、市长=金峰（朝鲜族，1981-03，2025-09-15任代市长，2026-01十九届人大五次会议当选）
  前任市委书记=赵永浩（2021-2025-01，2025-06-17被吉林省纪委监委查，2026-02-09被开除党籍和公职）
  前任市长=吴贤哲（2021-11十九届人大一次会议当选市长，后调任龙井市委书记）

Sources (一级/二级):
  - 延吉市人民政府官网（www.yanji.gov.cn）：市政府领导页（市长金峰+6位副市长简历）、领导活动、
    重要会议、延吉要闻（2026-02~2026-08 多篇常委会/会议报道点名王吉宝、金峰、裴海涛、赵泉江、吕家志、许永光等）
  - 澎湃新闻/网易/腾讯（2025-01）："王吉宝已任吉林延边州委常委、延吉市委书记"，含完整履历
  - 吉林省纪委监委官网（ccdijl.gov.cn）：赵永浩（2025-06-17 受查）、金时德（2025-02-20 查）、
    池龙云（2026-06 查）、刘岩智（2026-08-05 延边州人大常委会原副主任 查）等通报
  - 延边新闻网/中国吉林网/凤凰网（2025-09）："金峰任延吉市代市长"（市十九届人大常委会第27次主任会议提名）
  - 延吉新闻网（yanjinews.com）：延吉市十九届人大大事记（2021-11 吴哲当选市长；姜虎权任书记等历史）

Confidence:
  - 王吉宝（书记）：confirmed（官方报道2026年内在任 + 澎湃2025-01任前报道 + 个人简历）
  - 金峰（市长）：confirmed（官网简历 2026 在任 + 2025-09 代市长新闻）
  - 赵永浩（前任书记，被双开）：confirmed（吉林省纪委监委）
  - 吴哲（前任市长→现龙井市委书记）：confirmed（2021-11人大选举报道 + 龙井市委2026年报道）
  - 常委班子多数：confirmed（延吉官网2026年2-7月活动报道点名）
  - 石琦华（州委常委、统战部部长）：confirmed（州政府官网/搜狗百科2025-01）
  - 张守亮、李仁哲（政协副主席人选）：plausible（政协22次常委会报道）
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
_REPO = BASE
for _ in range(4):
    if (_REPO / "gov_relation").is_dir():
        break
    _REPO = _REPO.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build

SLUG = "延吉市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-11"
DB_PATH = str(BASE / f"{SLUG}_network.db")
GEXF_PATH = str(BASE / f"{SLUG}_network.gexf")

# ═══════════════════════════ Persons ═══════════════════════════
persons = [
    {"id": 1, "name": "王吉宝", "gender": "男", "ethnicity": "汉族", "birth": "1972年10月",
     "birthplace": "", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "州委常委、市委书记", "current_org": "中共延吉市委员会",
     "source": "澎湃新闻2025-01-30；延吉市人民政府官网2026-07（常委会/招商会报道）"},
    {"id": 2, "name": "金峰", "gender": "男", "ethnicity": "朝鲜族", "birth": "1981年3月",
     "birthplace": "", "education": "延边大学国际政治专业，研究生学历",
     "party_join": "2000年8月", "work_start": "2004年7月",
     "current_post": "市委副书记、市长", "current_org": "延吉市人民政府",
     "source": "http://www.yanji.gov.cn/szf_2462/szfld/sz/（市长简历）"},
    {"id": 3, "name": "裴海涛", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记", "current_org": "中共延吉市委员会",
     "source": "延吉市人民政府官网领导活动/延吉要闻（2026-07-28慰问驻延部队；2026-07-30主持理论学习中心组学习会）"},
    {"id": 4, "name": "赵泉江", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市纪委书记、市监委主任", "current_org": "中共延吉市纪律检查委员会",
     "source": "延吉市人民政府官网（2026-02-09 纪委全会；2026-07-24 走访慰问部队）"},
    {"id": 5, "name": "吕家志", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中共延吉市委组织部",
     "source": "延吉市人民政府官网（2026-03-25 全市组织工作会议，吕家志出席并讲话）"},
    {"id": 6, "name": "时佰林", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、宣传部部长", "current_org": "中共延吉市委宣传部",
     "source": "延吉新闻网2023-03；今日头条2026-07-21（延吉市委常委名单）"},
    {"id": 7, "name": "陈航发", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、政法委书记", "current_org": "中共延吉市委政法委员会",
     "source": "今日头条2026-07-21（延吉市委常委名单）"},
    {"id": 8, "name": "许永光", "gender": "男", "ethnicity": "朝鲜族", "birth": "1976年12月",
     "birthplace": "", "education": "延边大学国际贸易学专业硕士研究生",
     "party_join": "1998年11月", "work_start": "1999年8月",
     "current_post": "市委常委、统战部部长、市政协党组副书记（兼副市长）", "current_org": "中共延吉市委统战部",
     "source": "http://www.yanji.gov.cn/szf_2465/szfld/fsl/（简历）；延吉官网政协常委会报道（2026-07-03）"},
    {"id": 9, "name": "张学斌", "gender": "男", "ethnicity": "汉族", "birth": "1980年10月",
     "birthplace": "", "education": "延边大学宪法学与行政法学专业研究生，法学硕士",
     "party_join": "2007年6月", "work_start": "2002年7月",
     "current_post": "市委常委、市政府副市长", "current_org": "延吉市人民政府",
     "source": "http://www.yanji.gov.cn/szf_2465/szfld/（简历）；延吉市人大第31次会议报道（2026-08-05 列席）"},
    {"id": 10, "name": "杨飞", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "市委常委、市政府副市长（挂职）", "current_org": "延吉市人民政府",
     "source": "http://www.yanji.gov.cn/szf_2465/szfld/（挂职副市长）"},
    {"id": 11, "name": "文京春", "gender": "男", "ethnicity": "朝鲜族", "birth": "1975年12月",
     "birthplace": "", "education": "延边大学朝鲜语口译专业研究生",
     "party_join": "1998年5月", "work_start": "1996年7月",
     "current_post": "延边州公安局党委委员、副局长；延吉市副市长、市公安局党委书记、局长", "current_org": "延吉市公安局",
     "source": "http://www.yanji.gov.cn/szf_2465/szfld/（简历）；延吉新闻网2018（十八届人大37次会议任命）"},
    {"id": 12, "name": "嵇文波", "gender": "男", "ethnicity": "汉族", "birth": "1973年3月",
     "birthplace": "", "education": "延边大学宪法与行政法专业，法学硕士",
     "party_join": "2003年6月", "work_start": "1993年7月",
     "current_post": "市人民政府副市长", "current_org": "延吉市人民政府",
     "source": "http://www.yanji.gov.cn/szf_2465/szfld/（简历）"},
    {"id": 13, "name": "金银姬", "gender": "女", "ethnicity": "朝鲜族", "birth": "1986年9月",
     "birthplace": "", "education": "延边大学民族学专业硕士研究生",
     "party_join": "2016年6月", "work_start": "2011年4月",
     "current_post": "市人民政府副市长", "current_org": "延吉市人民政府",
     "source": "http://www.yanj.gov.cn/szf_2465/szfld/（简历，2025-02官网新增）"},
    {"id": 14, "name": "薛志强", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会主任", "current_org": "延吉市人民代表大会常务委员会",
     "source": "延吉市人民政府官网（2026-07-23 人大主任走访慰问报道；2026-08-05 人大31次会议报道）"},
    {"id": 15, "name": "禹军", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政协党组书记、主席", "current_org": "中国人民政治协商会议延吉市委员会",
     "source": "延吉市人民政府官网（2026-07-03 政协22次会议报道）"},
    {"id": 16, "name": "石琦华", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "延边州委常委、统战部部长", "current_org": "中共延边朝鲜族自治州委员会",
     "source": "延吉市人民政府官网（2026-07 赴延吉宣讲《民族团结进步促进法》）；吉林省人民政府网2024-09（州委常委、统战部部长确认）"},
    {"id": 17, "name": "赵永浩", "gender": "男", "ethnicity": "朝鲜族", "birth": "1973年2月",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "前任延吉市委书记（2021-2025-01）；后任吉林省国防动员办副主任（被双开）", "current_org": "",
     "source": "中安在线/腾讯新闻/新浪财经 2025-06-17（被查通报，含简历）；吉林省纪委监委 ccdijl.gov.cn 2026-02-09（双开通报）"},
    {"id": 18, "name": "吴贤哲", "gender": "男", "ethnicity": "朝鲜族（推定）", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任延吉市长（2021-11 当选）；现任龙井市委书记", "current_org": "中共龙井市委员会",
     "source": "人民网吉林/jl.people.com.cn 2021-11-30（延吉市十九届人大一次会议）；龙井市人民政府网 2026-05~07 报道"},
    {"id": 19, "name": "洪庆", "gender": "男", "ethnicity": "朝鲜族", "birth": "1976年11月",
     "birthplace": "", "education": "东北师范大学经济学博士",
     "party_join": "2000年7月", "work_start": "1999年9月",
     "current_post": "前任延吉市委书记（2019-07~2021-11）；现任吉林省人民政府秘书长", "current_org": "吉林省人民政府",
     "source": "Wikipedia《洪庆 (1976年)》；南方都市报2026-05（省政府秘书长）"},
    {"id": 20, "name": "金时德", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "延吉市人大常委会原副主任（2026-02 被查）", "current_org": "",
     "source": "吉林省纪委监委 ccdijl.gov.cn（2026-02-20 金时德被查通报）"},
    {"id": 21, "name": "池龙云", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "延吉市人大常委会党组副书记、副主任（2026-06 被查）", "current_org": "",
     "source": "吉林省纪委监委 ccdijl.gov.cn（2026-06 池龙云被查通报，经搜狗快照引用）"},
]

# ═══════════════════════════ Organizations ═══════════════════════════
organizations = [
    {"id": 1, "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地级(州)", "parent": "中共吉林省委员会", "location": "延边州"},
    {"id": 2, "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地级(州)", "parent": "吉林省人民政府", "location": "延边州"},
    {"id": 3, "name": "中共延吉市委员会", "type": "党委", "level": "县级", "parent": "中共延边朝鲜族自治州委员会", "location": "延吉市"},
    {"id": 4, "name": "延吉市人民政府", "type": "政府", "level": "县级", "parent": "延边朝鲜族自治州人民政府", "location": "延吉市"},
    {"id": 5, "name": "中共延吉市纪律检查委员会（含市监委）", "type": "党委", "level": "县级", "parent": "中共延吉市委员会", "location": "延吉市"},
    {"id": 6, "name": "中共延吉市委组织部", "type": "党委", "level": "县级", "parent": "中共延吉市委员会", "location": "延吉市"},
    {"id": 7, "name": "中共延吉市委宣传部", "type": "党委", "level": "县级", "parent": "中共延吉市委员会", "location": "延吉市"},
    {"id": 8, "name": "中共延吉市委统战部", "type": "党委", "level": "县级", "parent": "中共延吉市委员会", "location": "延吉市"},
    {"id": 9, "name": "中共延吉市委政法委员会", "type": "党委", "level": "县级", "parent": "中共延吉市委员会", "location": "延吉市"},
    {"id": 10, "name": "延吉市公安局", "type": "政府", "level": "县级", "parent": "延吉市人民政府", "location": "延吉市"},
    {"id": 11, "name": "延吉市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "延边州人大常委会", "location": "延吉市"},
    {"id": 12, "name": "中国人民政治协商会议延吉市委员会", "type": "政协", "level": "县级", "parent": "延边州政协", "location": "延吉市"},
    {"id": 13, "name": "延吉市发展和改革局（市粮食和物资储备局）", "type": "政府", "level": "县级", "parent": "延吉市人民政府", "location": "延吉市"},
    {"id": 14, "name": "延吉市人民法院", "type": "司法", "level": "县级", "parent": "", "location": "延吉市"},
    {"id": 15, "name": "延吉市人民检察院", "type": "司法", "level": "县级", "parent": "", "location": "延吉市"},
    {"id": 16, "name": "中共安图县委员会", "type": "党委", "level": "县级", "parent": "中共延边朝鲜族自治州委员会", "location": "安图县"},
    {"id": 17, "name": "延吉市（前和龙市）人民政府", "type": "政府", "level": "县级", "parent": "延边朝鲜族自治州人民政府", "location": "和龙市"},
    {"id": 18, "name": "中共龙井市委员会", "type": "党委", "level": "县级", "parent": "中共延边朝鲜族自治州委员会", "location": "龙井市"},
    {"id": 19, "name": "吉林省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长春市"},
    {"id": 20, "name": "吉林省国防动员办公室（省人民防空办公室）", "type": "政府", "level": "省级", "parent": "吉林省人民政府", "location": "长春市"},
]

# ═══════════════════════════ Positions ═══════════════════════════
positions = [
    # 王吉宝
    {"person_id": 1, "org_id": 1, "title": "州委常委（兼延吉市委书记）", "start_date": "2025-01", "end_date": "present", "rank": "副厅级", "note": "延边州委常委、延吉市委书记"},
    {"person_id": 1, "org_id": 3, "title": "市委书记", "start_date": "2025-01", "end_date": "present", "rank": "县处级正职（州委常委兼）", "note": "2025年1月任（澎湃/网易2025-01-30）"},
    {"person_id": 1, "org_id": 16, "title": "安图县委书记", "start_date": "2021-09", "end_date": "2024-10", "rank": "县处级正职", "note": "2021-09-30当选十六届县委委员全会上；2024-11 陈铨继任"},
    {"person_id": 1, "org_id": 2, "title": "州农业农村局党组书记、局长", "start_date": "unknown", "end_date": "2021-08", "rank": "正处级", "note": "任延吉市委书记前为州农业农村局负责人"},
    # 金峰
    {"person_id": 2, "org_id": 4, "title": "市委副书记、市长", "start_date": "2026-01", "end_date": "present", "rank": "县处级正职", "note": "2026-01 市十九届人大五次会议当选"},
    {"person_id": 2, "org_id": 4, "title": "市委副书记、代市长", "start_date": "2025-09-15", "end_date": "2026-01", "rank": "县处级正职", "note": "经第十九届人大常委会第27次主任会议提名，2025年9月15日（凤凰网/网易）"},
    {"person_id": 2, "org_id": 4, "title": "市人民政府副市长", "start_date": "2025-08", "end_date": "2025-09-15", "rank": "副处级", "note": "市十九届人大常委会第24次会议任命"},
    {"person_id": 2, "org_id": 13, "title": "市发改局党组书记、局长", "start_date": "2021-09", "end_date": "2025-08", "rank": "正科级（市局局长）", "note": "2021-09-24 十八届人大常委会第37次会议任命为市发改局局长（市粮食和物资储备局）"},
    # 裴海涛
    {"person_id": 3, "org_id": 3, "title": "市委副书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "2026-07主持理论学习中心组集体学习会；八一前走访慰问部队"},
    # 赵泉江
    {"person_id": 4, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "2026-02-09 市纪委十六届六次全会主持并作工作报告"},
    # 吕家志
    {"person_id": 5, "org_id": 6, "title": "市委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "2026-03-25 全市组织工作会议出席并讲话"},
    # 时佰林
    {"person_id": 6, "org_id": 7, "title": "市委常委、宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "2023-03 宣传思想文化工作会议作报告；2026-07 仍在任"},
    # 陈航发
    {"person_id": 7, "org_id": 9, "title": "市委常委、政法委书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "2026-07-21 报道"},
    # 许永光
    {"person_id": 8, "org_id": 8, "title": "市委常委、统战部部长（兼市政协党组副书记）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "2026-07-03 政协22次会议以市委常委、统战部部长、市政协党组副书记身份主持"},
    {"person_id": 8, "org_id": 4, "title": "市人民政府副市长（兼）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "市政府领导名单6名副市长之一"},
    # 张学斌
    {"person_id": 9, "org_id": 4, "title": "市委常委、市政府副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "2026-08-05 人大31次会议列席"},
    {"person_id": 9, "org_id": 3, "title": "市委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨飞
    {"person_id": 10, "org_id": 4, "title": "市委常委、市政府副市长（挂职）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 文京春
    {"person_id": 11, "org_id": 10, "title": "副市长、市公安局党委书记、局长", "start_date": "2021-09", "end_date": "present", "rank": "副处级", "note": "2021-09-24 十八届人大常委会第37次会议任命"},
    {"person_id": 11, "org_id": 2, "title": "州公安局党委委员、副局长（兼）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 嵇文波
    {"person_id": 12, "org_id": 4, "title": "市人民政府副市长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    # 金银姬
    {"person_id": 13, "org_id": 4, "title": "市人民政府副市长", "start_date": "2025-02", "end_date": "present", "rank": "副处级", "note": "2025-02上线领导之窗"},
    # 薛志强
    {"person_id": 14, "org_id": 11, "title": "市人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "2026-07-23 走访慰问；2026-08-05 人大31次会议主持"},
    # 禹军
    {"person_id": 15, "org_id": 12, "title": "市政协党组书记、主席", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "2026-07-03 政协22次会议主持"},
    # 石琦华
    {"person_id": 16, "org_id": 1, "title": "州委常委、统战部部长", "start_date": "2022", "end_date": "present", "rank": "副厅级", "note": "2026-07 赴延吉宣讲民族团结进步法"},
    # 赵永浩
    {"person_id": 17, "org_id": 20, "title": "省国防动员办公室党组成员、副主任", "start_date": "2025-01", "end_date": "2025-06-17", "rank": "副厅级", "note": "2025年被查"},
    {"person_id": 17, "org_id": 3, "title": "延吉市委书记（前任）", "start_date": "2021-12", "end_date": "2025-01", "rank": "副厅级", "note": "2021年12月前后接替洪劭；2025-01王吉宝接任"},
    {"person_id": 17, "org_id": 5, "title": "延边州纪委副书记（此前）", "start_date": "unknown", "end_date": "2021", "rank": "副厅级", "note": "曾任州纪委副书记等"},
    # 吴贤哲
    {"person_id": 18, "org_id": 18, "title": "龙井市委书记（现任）", "start_date": "2025-09", "end_date": "present", "rank": "县处级正职", "note": "2025-09后调龙井（2026-05~07 龙井官网多篇报道确认）"},
    {"person_id": 18, "org_id": 4, "title": "延吉市市长（前任）", "start_date": "2021-11", "end_date": "2025-08", "rank": "县处级正职", "note": "2021-11-29 延吉市十九届人大五次会议当选"},
    # 洪庆
    {"person_id": 19, "org_id": 19, "title": "吉林省人民政府秘书长", "start_date": "2026-05", "end_date": "present", "rank": "正厅级", "note": "2026-04省政府党组成员"},
    {"person_id": 19, "org_id": 3, "title": "延吉市委书记（前任）", "start_date": "2019-07", "end_date": "2021-11", "rank": "副处级（州委常委兼）", "note": "州委常委兼延吉市委书记"},
    # risk 金时德/池龙云
    {"person_id": 20, "org_id": 11, "title": "市人大常委会副主任（原）", "start_date": "unknown", "end_date": "2026-02", "rank": "副处级", "note": "2026-02-20 被查"},
    {"person_id": 21, "org_id": 11, "title": "市人大常委会党组副书记、副主任（原）", "start_date": "unknown", "end_date": "2026-06", "rank": "副处级", "note": "2026-06 被查"},
]

# ═══════════════════════════ Relationships ═══════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "决策搭档", "context": "州委常委、市委书记与市委副书记、市长，党政主要领导搭档（2025-01至今）", "overlap_org": "中共延吉市委/延吉市人民政府", "overlap_period": "2025-01~present"},
    {"person_a": 1, "person_b": 3, "type": "班子/上下级", "context": "市委书记与专职副书记同处常委会（2026-07召开理论学习中心组学习会等）", "overlap_org": "中共延吉市委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "班子/上下级", "context": "市委书记与市纪委书记赵泉江，2026年第16次常委会（赵泉江汇报）", "overlap_org": "中共延吉市委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "班子/上下级", "context": "组织部长吕家志参加市委常委会", "overlap_org": "中共延吉市委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "班子/上下级", "context": "统战部长许永光参加市委常委会", "overlap_org": "中共延吉市委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 9, "type": "班子/上下级", "context": "常委副市长张学斌参加市委常委会", "overlap_org": "中共延吉市委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 17, "type": "前任-继任", "context": "王吉宝2025-01接任延吉市委书记；前书记赵永浩2025年6月被查，2026-02被双开（风险关联）", "overlap_org": "中共延吉市委", "overlap_period": "2025"},
    {"person_a": 17, "person_b": 19, "type": "前任-继任", "context": "洪庆（2019-07~2021-11 延州书记）→赵永浩（2021-12接任）→王吉宝（2025-01）", "overlap_org": "中共延吉市委", "overlap_period": "2021"},
    {"person_a": 2, "person_b": 18, "type": "前任-继任", "context": "金峰2025-09接任代市长/2026-01任市长；前任市长吴哲调任龙井市委书记", "overlap_org": "延吉市人民政府", "overlap_period": "2025-09"},
    {"person_a": 18, "person_b": 1, "type": "工作交集", "context": "吴哲（龙井书记）与王吉宝（延吉书记）同为延边州下辖县市委书记，州委统一领导", "overlap_org": "中共延边朝鲜族自治州委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 16, "type": "班子/上下级", "context": "州委常委王吉宝与州委常委、统战部长石琦华同在州委常委会", "overlap_org": "中共延边朝鲜族自治州委员会", "overlap_period": "2025-01~present"},
    {"person_a": 1, "person_b": 19, "type": "工作交集", "context": "两人先后任延吉市委书记（州委常委兼）；2019-07~2021-11洪庆、2025-01起王吉宝", "overlap_org": "中共延吉市委", "overlap_period": "跨期"},
    {"person_a": 2, "person_b": 9, "type": "班子/上下级", "context": "市长金峰与市委常委、副市长张学斌在政府班子内", "overlap_org": "延吉市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "班子/上下级", "context": "副市长、公安局长文京春，市政府班子（2021-09任命）", "overlap_org": "延吉市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "班子/上下级", "context": "副市长许永光（兼统战部长）", "overlap_org": "延吉市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "班子/上下级", "context": "副市长金银姬2025-02起在任", "overlap_org": "延吉市人民政府", "overlap_period": "present"},
    {"person_a": 17, "person_b": 20, "type": "风险关联", "context": "延吉市人大原副主任金时德2026-02被查（同市腐败链条）", "overlap_org": "延吉市人大", "overlap_period": "2021-2026"},
    {"person_a": 17, "person_b": 21, "type": "风险关联", "context": "延吉市人大党组副书记、副主任池龙云2026-06被查（赵永浩案串联）", "overlap_org": "延吉市人大", "overlap_period": "2021-2026"},
]

# ═══════════════════════════ Person JSON ═══════════════════════════
SOURCE_REGISTER = [
    {"id": "S001", "title": "延吉市人民政府·市政府领导（市长/副市长简历）", "url": "http://www.yanji.gov.cn/szf_2465/szfld/", "publisher": "延吉市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "金峰（市长，朝鲜族1981-03/延边大学国际政治）及六位副市长简历"},
    {"id": "S002", "title": "延吉市人民政府·领导活动（2026-04~08）", "url": "http://www.yanji.gov.cn/szf_2465/ldhd/", "publisher": "延吉市人民政府", "published_at": "2026-04~08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "薛志强(07-23)、裴海涛(07-28)、许永光(07-28)、赵泉丹(07-24)、杨飞(07-27)等走访慰问"},
    {"id": "S003", "title": "延吉市人民政府·重要会议（市委常委会/纪委全会/组织工作会）", "url": "http://www.yanji.gov.cn/szf_2465/zyhy/", "publisher": "延吉市人民政府", "published_at": "2026-02~08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王吉宝主持常委会（第9/13/16次）；赵泉江纪委全会主持；吕家志组织工作会议"},
    {"id": "S004", "title": "澎湃新闻：王吉宝已任延边州委常委、延吉市委书记", "url": "https://www.thepaper.cn/（经360/网易转载快照）", "publisher": "澎湃新闻", "published_at": "2025-01-30", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "王吉宝简历（1972-10、省委党校研究生；州卫计委党委副书记/和龙副市、常务副书记/州农业农村局局长→安图 2021→延吉 2025）"},
    {"id": "S005", "title": "网易订阅：金峰已任延吉市代市长", "url": "https://www.163.com/touch/article.html（或凤凰网转载）", "publisher": "延吉人大/中国吉林网（网易转载）", "published_at": "2025-09-15", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "经市十九届人大常委会第27次主任会议提名，表决通过金峰为代理市长"},
    {"id": "S006", "title": "人民网吉林频道：延吉市十九届人大五次会议选举报道", "url": "http://jl.people.com.cn/", "publisher": "人民网", "published_at": "2021-11-29", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "吴哲选市长（2021-11）"},
    {"id": "S007", "title": "吉林省纪委监委官网：审查调查通报", "url": "http://ccdijl.gov.cn/scdc/", "publisher": "吉林省纪委、省监委", "published_at": "2025-02-20~2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "金时德(2025-02-20)、池龙云(2026-06)、刘岩智(2026-08-05)、韩长发(2025-11-03)等；赵永浩双开通报(2026-02-09)"},
    {"id": "S008", "title": "延吉新闻网/延吉政府网：延吉市两会/人大大事记", "url": "http://www.yanjinews.com/", "publisher": "延吉市融媒体中心", "published_at": "2023-2026", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "时为宣传部长（2023-03）等"},
]


def build_person_file(name, current_post, identity, timeline, relations, orgs, big_gap, qs=None):
    p = BASE / f"{TODAY}-吉林省-延边朝鲜族自治州-{current_post}-{name}.json"
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "吉林省", "city": "延边朝鲜族自治州", "region": "延吉市",
                                "job": current_post, "task_id": "jilin_延吉市", "time_focus": "2019-2026"},
        "identity": {"person_id": f"yanji_{name}", "name": name, "aliases": [],
                     "gender": identity.get("gender", ""), "ethnicity": identity.get("ethnicity", ""),
                     "birth": identity.get("birth", ""), "birthplace": identity.get("birthplace", ""),
                     "native_place": identity.get("native_place", ""),
                     "education": identity.get("education", []),
                     "party_join": identity.get("party_join", ""), "work_start": identity.get("work_start", ""),
                     "dedupe_keys": {"name_birth": f"{name}_{identity.get('birth','')}",
                                     "name_birthplace": f"{name}_{identity.get('birthplace','')}",
                                     "official_profile_url": identity.get("official_profile_url", "")}},
        "current_status": {"current_post": current_post, "current_org": identity.get("current_org", ""),
                           "administrative_rank": identity.get("rank", ""), "as_of": AS_OF,
                           "is_current_confirmed": identity.get("is_current_confirmed", True),
                           "source_ids": identity.get("source_ids", ["S001"])},
        "career_timeline": timeline if timeline else [],
        "organizations": orgs if isinstance(orgs, list) else ([orgs] if orgs else []),
        "relationships": relations if isinstance(relations, list) else [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {"identity": "confirmed" if identity.get("birth") else "plausible",
                               "current_role": identity.get("current_role_conf", "confirmed"),
                               "career_completeness": "complete" if len(timeline or []) > 5 else ("partial" if timeline else "thin"),
                               "relationship_confidence": "medium", "biggest_gap": big_gap},
        "open_questions": qs or [{"priority": "critical", "question": big_gap, "why_it_matters": "任职网络分析",
                                  "suggested_queries": [f"{name} 简历"], "last_attempted": AS_OF}],
    }
    with open(p, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    print("  person JSON:", p.name)


def write_persons_files():
    # ── 王吉宝（现任市委书记） ──
    build_person_file(
        "王吉宝", "市委书记",
        {"gender": "男", "ethnicity": "汉族", "birth": "1972年10月", "birthplace": "",
         "native_place": "",
         "education": [{"period": "", "institution": "吉林省委党校", "major": "", "degree": "研究生学历", "study_type": "part_time", "source_ids": ["S004"]}],
         "party_join": "中共党员", "work_start": "", "current_org": "中共延吉市委员会",
         "rank": "州委常委、书记（副厅级）", "is_current_confirmed": True, "source_ids": ["S002", "S003", "S004"]},
        [{"start": "2025-01", "end": "present", "org": "中共延吉市委员会", "title": "州委常委、市委书记", "level": "县级", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "2025-01履新；2026年内多次主持市委常委会（2026年第16次等）", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
         {"start": "2021-09", "end": "2024-10", "org": "中共安图县委员会", "title": "县委书记", "level": "县级", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2021-09-30当选安图县十六届县委委员全；2024-11陈墩接任", "confidence": "confirmed", "source_ids": ["S004"]},
         {"start": "unknown", "end": "2021-08", "org": "延边州农业农村局", "title": "州农业农村局党组书记、局长", "level": "地级(州)", "system": "government", "rank": "正处级", "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
         {"start": "unknown", "end": "unknown", "org": "中共和龙市委员会/和龙市人民政府", "title": "和龙市委常委、常务副市长→常务副书记", "level": "县级", "system": "party", "rank": "正科-副处级", "notes": "", "confidence": "confirmed", "source_ids": ["S004"]},
         {"start": "unknown", "end": "unknown", "org": "延边州卫生局", "title": "州卫生局党委副书记等", "level": "州级", "system": "party", "rank": "", "notes": "早期卫生系统", "confidence": "confirmed", "source_ids": ["S004"]}],
        [{"person": "金峰", "person_id": "yanji_金峰", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "书记与市长党政搭档（2025-01 至今）", "overlap_org": "中共延吉市委/延吉市人民政府", "overlap_period": "2025-01~present", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
         {"person": "赵永浩", "person_id": "yanji_赵永浩", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任书记赵永浩2025-01离任后被查；王吉宝接任", "overlap_org": "中共延吉市委", "overlap_period": "2025-01", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004", "S007"]},
         {"person": "石琦华", "person_id": "yanji_石琦华", "relationship_type": "work_intersection", "strength": "medium", "evidence": "同为延边州委常委（州委会议交集）", "overlap_org": "中共延边州委", "overlap_period": "2025-01~present", "direction": "undirected", "confidence": "plausible", "source_ids": ["S002"]},
         {"person": "吴贤哲", "person_id": "yanji_吴贤哲", "relationship_type": "work_intersection", "strength": "medium", "evidence": "延吉市委书记与龙井市委书记，州委统一领导下县市交流", "overlap_org": "中共延边州委", "overlap_period": "present", "direction": "undirected", "confidence": "plausible", "source_ids": ["S006"]}],
        [{"id": "yanji_市委", "name": "中共延吉市委员会", "type": "党委", "level": "县级", "location": "延吉市"},
         {"id": "yanji_安图县委", "name": "中共安图县委员会", "type": "党委", "level": "县级", "location": "安图县"}],
        "王吉宝出生地、入党时间、具体晋升年份（和龙时期时间节点）待补；2025-01履新前的过渡任职（2024-10~2025-01）",
        [{"priority": "medium", "question": "王吉宝与赵永浩的关系（是否同窗/同科室）", "why_it_matters": "涉腐链条可能延及现任书记任内", "suggested_queries": ["王吉宝 赵永浩 关系"], "last_attempted": AS_OF}],
    )

    # ── 金峰（现任市长） ──
    build_person_file(
        "金峰", "市长",
        {"gender": "男", "ethnicity": "朝鲜族", "birth": "1981年3月", "birthplace": "",
         "native_place": "",
         "education": [{"period": "", "institution": "延边大学", "major": "国际政治", "degree": "研究生学历", "study_type": "unknown", "source_ids": ["S001"]}],
         "party_join": "2000年8月", "work_start": "2004年7月", "current_org": "延吉市人民政府",
         "rank": "县处级正职", "is_current_confirmed": True, "source_ids": ["S001", "S005"]},
        [{"start": "2026-01", "end": "present", "org": "延吉市人民政府", "title": "市委副书记、市长", "level": "县级", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-01 市十九届人大五次会议当选；2026-07 主持招商会部署", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
         {"start": "2025-09-15", "end": "2026-01", "org": "延吉市人民政府", "title": "市委副书记、代市长", "level": "县级", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
         {"start": "2025-08", "end": "2025-09-15", "org": "延吉市人民政府", "title": "市人民政府副市长", "level": "县级", "system": "government", "rank": "副处级", "notes": "", "confidence": "confirmed", "source_ids": ["S005"]},
         {"start": "2021-09", "end": "2025-08", "org": "延吉市发展和改革局", "title": "市发改局党组书记、局长", "level": "县级", "system": "government", "rank": "正科级（市局）", "notes": "主持市发改局（市粮食和物资储备局）", "confidence": "confirmed", "source_ids": ["S005"]}],
        [{"person": "王吉宝", "person_id": "yanji_王吉宝", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "市长在书记领导下工作，党政搭档", "overlap_org": "延吉市人民政府", "overlap_period": "2025-01~present", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
         {"person": "吴贤哲", "person_id": "yanji_吴贤哲", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任市长吴贤哲2025-09卸任调龙井，金峰接任", "overlap_org": "延吉市人民政府", "overlap_period": "2025-09", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S006"]},
         {"person": "张学斌", "person_id": "yanji_张学斌", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "常委副市长与市长同政府班子", "overlap_org": "延吉市人民政府", "overlap_period": "present", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]}],
        [{"id": "yanji_市政府", "name": "延吉市人民政府", "type": "政府", "level": "县级", "location": "延吉市"},
         {"id": "yanji_发改局", "name": "延吉市发展和改革局", "type": "政府", "level": "县级", "location": "延吉市"}],
        "金峰新婚出生地/入党前工作单位、发改局长的完整经历（2004-2021年）",
        [{"priority": "high", "question": "金峰 2004-2021 年间的早期职务（2004工作→2021发改局长，17年空缺）", "why_it_matters": "评估其晋升路径（有无州机关/乡镇长经历）", "suggested_queries": ["金峰 延吉 简历 发改", "金峰 延吉 乡镇"], "last_attempted": AS_OF}],
    )

    # ── 赵永浩（前任市委书记，被双开） ──
    build_person_file(
        "赵永浩", "前任市委书记",
        {"gender": "男", "ethnicity": "朝鲜族", "birth": "1973年2月", "birthplace": "",
         "native_place": "",
         "education": [{"period": "", "institution": "", "major": "", "degree": "硕士研究生", "study_type": "unknown", "source_ids": ["S004"]}],
         "party_join": "中共党员", "work_start": "", "current_org": "",
         "rank": "省国防动员办公室原副主任（副厅级）", "is_current_confirmed": False, "source_ids": ["S004", "S007"]},
        [{"start": "2025-01", "end": "2025-06-17", "org": "吉林省国防动员办（省人防办）", "title": "党组成员、副主任", "level": "省级", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "2025-06-17 被查", "confidence": "confirmed", "source_ids": ["S007"]},
         {"start": "2021-12", "end": "2025-01", "org": "中共延吉市委员会", "title": "延吉市委书记（州委常委兼）", "level": "县级", "system": "party", "rank": "副厅级", "is_key_promotion": True, "notes": "接替洪庆", "confidence": "confirmed", "source_ids": ["S004", "S007"]},
         {"start": "unknown", "end": "2021-12", "org": "图们市/延边州纪委", "title": "图们市长/市委书记等；州纪委副书记", "level": "县级", "system": "party", "rank": "正处-副厅级", "notes": "曾任州纪委副书记（中央巡1m3期间被查）", "confidence": "confirmed", "source_ids": ["S007"]}],
        [{"person": "王吉宝", "person_id": "yanji_王吉宝", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "王吉宝2025-01接任其市委书记位", "overlap_org": "中共延吉市委", "overlap_period": "2025-01", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004", "S007"]},
         {"person": "洪庆", "person_id": "yanji_洪庆", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "洪庆2019-07~2021-11任延吉书记后赵永浩接任", "overlap_org": "中共延吉市委", "overlap_period": "2021", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]},
         {"person": "金峰", "person_id": "yanji_金峰", "relationship_type": "work_intersection", "strength": "medium", "evidence": "赵任书记期间金峰任市发改局局长（2021-2025）", "overlap_org": "延吉市人民政府", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "plausible", "source_ids": ["S005"]}],
        [{"id": "yanji_市委", "name": "中共延吉市委员会", "type": "党委", "level": "县级", "location": "延吉市"},
         {"id": "jilin_省国动办", "name": "吉林省国防动员办", "type": "政府", "level": "省级", "location": "长春市"}],
        "赵永浩违纪具体案由（双开通报摘要）；其与金寿浩（前州长）、池龙云/金时德（延吉市人大）的关联证据",
        [{"priority": "critical", "question": "赵永浩案是否涉及现任延吉市委领导（王吉宝/金峰）？", "why_it_matters": "若涉腐链条延伸，将影响延吉市现任班子稳定", "suggested_queries": ["赵永浩 双开 通报 详情", "延吉市 腐败 链条 2026"], "last_attempted": AS_OF}],
    )

    # ── 吴贤哲（前任市长 → 现任龙井市委书记） ──
    build_person_file(
        "吴贤哲", "前任市长",
        {"gender": "男", "ethnicity": "朝鲜族（推定）", "birth": "", "birthplace": "",
         "native_place": "",
         "education": [], "party_join": "中共党员", "work_start": "", "current_org": "中共龙井市委员会",
         "rank": "县处级正职（曾任延吉市长）", "is_current_confirmed": False, "source_ids": ["S006", "S002"]},
        [{"start": "2025-09", "end": "present", "org": "中共龙井市委员会", "title": "龙井市委书记", "level": "县级", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2025-09后调任龙井（2026-05~07龙井）多篇活动报道确定）", "confidence": "confirmed", "source_ids": ["S002"]},
         {"start": "2021-11", "end": "2025-08", "org": "延吉市人民政府", "title": "延吉市市长", "level": "县级", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "2021-11-29 延吉市十九届人大五次会议当选；2025-09金峰任代市长", "confidence": "confirmed", "source_ids": ["S006"]}],
        [{"person": "金峰", "person_id": "yanji_金峰", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "吴贤哲→金峰市长交接（2025-09）", "overlap_org": "延吉市人民政府", "overlap_period": "2025-09", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S006"]},
         {"person": "王吉宝", "person_id": "yanji_王吉宝", "relationship_type": "work_intersection", "strength": "medium", "evidence": "同为延边州下辖县市一把手（州统一领导）", "overlap_org": "中共延边州委", "overlap_period": "present", "direction": "undirected", "confidence": "plausible", "source_ids": []}],
        [{"id": "yanji_市政府", "name": "延吉市人民政府", "type": "政府", "level": "县级", "location": "延吉市"},
         {"id": "yanji_龙井市委", "name": "中共龙井市委员会", "type": "党委", "level": "县级", "location": "龙井市"}],
        "吴哲出生年月、民族确证、完整履历（2021前及2025年调任龙井的具体时间）",
    )

    # ── 裴海涛（市委副书记） ──
    build_person_file(
        "裴海涛", "市委副书记",
        {"gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "native_place": "", "education": [], "party_join": "中共党员", "work_start": "",
         "current_org": "中共延吉市委员会", "rank": "副处级", "is_current_confirmed": True, "source_ids": ["S002", "S003"]},
        [{"start": "unknown", "end": "present", "org": "中共延吉市委员会", "title": "市委副书记", "level": "县级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "2026-07-30主持理论学习中心组集体学习会；07-28走访慰问驻军部队", "confidence": "confirmed", "source_ids": ["S002", "S003"]}],
        [{"person": "王吉宝", "person_id": "yanji_王吉宝", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "副书记协助书记分管党务", "overlap_org": "中共延吉市委", "overlap_period": "present", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"id": "yanji_市委", "name": "中共延吉市委员会", "type": "党委", "level": "县级", "location": "延吉市"}],
        "裴海涛出生年月、学历、完整履历",
    )

    # ── 赵泉江（市纪委书记、监委主任） ──
    build_person_file(
        "赵泉江", "市纪委书记、市监委主任",
        {"gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
         "native_place": "", "education": [], "party_join": "中共党员", "work_start": "",
         "current_org": "中共延吉市纪律检查委员会", "rank": "副处级", "is_current_confirmed": True, "source_ids": ["S003"]},
        [{"start": "unknown", "end": "present", "org": "中共延吉市纪律检查委员会", "title": "市委常委、市纪委书记、市监委主任", "level": "县级", "system": "party", "rank": "副处级", "is_key_promotion": True, "notes": "2026-02-09 市纪委十六届六中全会主持并作报告", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"person": "王吉宝", "person_id": "yanji_王吉宝", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "纪委受市委领导，书记向市委常委会汇报", "overlap_org": "中共延吉市委", "overlap_period": "present", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"id": "yanji_市纪委", "name": "中共延吉市委纪律检查委员会", "type": "党委", "level": "县级", "location": "延吉市"}],
        "赵泉江的履历与出生信息；其何时到延吉任职",
    )

    # ── 张学斌（市委常委、副市长） ──
    build_person_file(
        "张学斌", "常委、副市长",
        {"gender": "男", "ethnicity": "汉族", "birth": "1980年10月", "birthplace": "",
         "native_place": "",
         "education": [{"period": "", "institution": "延边大学", "major": "宪法学与行政法学", "degree": "法学硕士", "study_type": "unknown", "source_ids": ["S001"]}],
         "party_join": "2007年6月", "work_start": "2002年7月", "current_org": "延吉市人民政府",
         "rank": "副处级", "is_current_confirmed": True, "source_ids": ["S001"]},
        [{"start": "unknown", "end": "present", "org": "延吉市人民政府", "title": "市委常委、市政府副市长", "level": "县级", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "2026-08-05 列席市人大第31次会议", "confidence": "confirmed", "source_ids": ["S001", "S003"]}],
        [{"person": "金峰", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "副市长在市长领导下工作", "overlap_org": "延吉市人民政府", "overlap_period": "present", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]}],
        [{"id": "yanji_市政府", "name": "延吉市人民政府", "type": "政府", "level": "县级", "location": "延吉市"}],
        "张学斌任副市长的时间与任职前经历",
    )


def main():
    print(f"[{SLUG}] 构建 SQLite DB + GEXF ...")
    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=DB_PATH, gexf_path=GEXF_PATH)
    _verify_db()
    write_persons_files()
    print(f"[{SLUG}] 完成：{DB_PATH}\n{GEXF_PATH}\npersons JSON 若干")


def _verify_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required = {"persons", "organizations", "positions", "relationships"}
        missing = sorted(required - tables)
        if missing:
            raise SystemExit(f"DB 缺少表: {missing}")
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in sorted(required)}
        print(f"  DB 校验: {counts}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()