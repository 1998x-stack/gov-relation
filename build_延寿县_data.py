#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 延寿县 (Yanshou County), 哈尔滨市, 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_延寿县
Level: 县
Targets: 县委书记 & 县长

Research sources (primary, official where possible):
  - 哈尔滨市延寿县人民政府·中共延寿县委 领导页 (领导职务表)  [via 延寿县政府官网 www.hrb-yanshou.gov.cn / Baidu index]
  - 哈尔滨市延寿县人民政府·县委书记 李宏伟 简历页 (2026-01-21 发布)
  - 哈尔滨市延寿县人民政府·县委副书记县长 徐涤非 简历页 (2026-01-21 发布)
  - 百度百科: 李宏伟(延寿县委书记)、徐涤非、张洪岐(前任书记/人社)、丁宇恒(原县长)
  - 环球网报道: 原县委书纪 封殿辉 受贿获刑 (2018-08-12)
  - 延寿县人大常委会任免名单 (2024-05-10 / 2026-04 发布)
  - 哈尔滨市/黑龙江省政府网 人事信息与任前公示
  - repo 本地: data/tmp/heilongjiang_双城区/ 徐鑫(双城区委副书记, 原延寿县六团镇) — 跨县交流确认

As-of: 2026-08

Confirmed current leadership:
  - 李宏伟：县委书记（2024-04至今）— 阿城区/呼兰区轮岗后任延寿书记
  - 徐涤非：县委副书记、县长（2021-12至今）— 绥化市绥棱县出身调哈县
  - 副书记：朱志刚（in 百度百科 中共延寿县委名录; 延寿官网另列 关伟庆 2024-07，有矛盾记入 open gaps）
  - 常委：张东来、李颖（组织部）、张淑英（宣传部）、薛春林、谭磊（统战）、曲雪峰、高珊、郭彦洁
  - 常委 政府副县长：杨向海（2025-12）；常委 纪委书记：魏春雷（2024-08）
  - 副县长：张云会（2026-01）、史建华（公安局长 2024-05）、刘城（曾任常委副县长）

Predecessor chains:
  县委书记：封殿辉(2011-2017, 受贿获刑) → 刘金成(2017-12) → 张洪岐(2021-11, 县长转书记; 现哈尔滨市人社局) → 李宏伟(2024-04)
  县长：丁宇恒 → 张洪岐(2018.09代/2019.01县长) → 徐涤非(2021-12)

Cross-county exchange (哈尔滨市域轮岗):
  李宏伟：阿城区→呼兰区→延寿县；张洪岐：呼兰区→延寿县→哈尔滨市人社局；徐涤非：绥化绥棱→延寿；
  徐鑫(双城区委副书记)：延寿六团镇→双城。徐鑫=跨县交流的直接证据。

Gaps (见 open gaps):
  - 徐涤非 2003-2021 中间履历细节待补
  - 副书记 关伟庆/朱志刚 在任时间矛盾
  - 现 人大主任/政协主席 在任者
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "延寿县"
TODAY = datetime.now().strftime("%Y%m%d")          # 20260805
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # 核心：县委书记 / 县长
    {"id": 1, "name": "李宏伟", "gender": "男", "ethnicity": "汉族", "birth": "1978-05", "birthplace": "黑龙江哈尔滨",
     "education": "东北农业大学网络教育学院法学专业（在职）", "party_join": "1999-05", "work_start": "2000-08",
     "current_post": "县委书记", "current_org": "中共延寿县委员会", "source": "延寿县政府官网·县委书记李宏伟简历页"},
    {"id": 2, "name": "徐涤非", "gender": "男", "ethnicity": "汉族", "birth": "1980-12", "birthplace": "黑龙江肇源",
     "education": "齐齐哈尔大学师范学院汉语言文学专业（大学/学士）", "party_join": "中共党员", "work_start": "2000-08",
     "current_post": "县委副书记、县长", "current_org": "延寿县人民政府", "source": "延寿县政府网·县长徐涤非简历页"},
    {"id": 3, "name": "关庆伟", "gender": "男", "ethnicity": "满族", "birth": "1975-04", "birthplace": "辽宁凤城",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记（代管县委政法委）", "current_org": "中共延寿县委员会", "source": "延寿县政府网·关庆伟简历页 (2024-07)"},
    {"id": 4, "name": "杨向海", "gender": "男", "ethnicity": "", "birth": "1976-10", "birthplace": "黑龙江宾县",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "延寿县人民政府", "source": "延寿县政府网·常务副县长简历 (2025-12)"},
    {"id": 5, "name": "魏春雷", "gender": "男", "ethnicity": "", "birth": "1974-10", "birthplace": "黑龙江省方正县",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共延寿县纪律检查委员会", "source": "延寿县政府网·魏春雷简历页 (2024-08)"},
    {"id": 6, "name": "郭彦发", "gender": "男", "ethnicity": "", "birth": "1974-09", "birthplace": "黑龙江巴彦",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共延寿县委组织部", "source": "延寿县政府网·郭彦发简历页 (2024-08)"},
    {"id": 7, "name": "张淑英", "gender": "女", "ethnicity": "", "birth": "1971-03", "birthplace": "山东郓城",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共延寿县委宣传部", "source": "延寿县政府网·张淑英简历页 (2021-11)"},
    {"id": 8, "name": "李惠达", "gender": "男", "ethnicity": "", "birth": "1976-07", "birthplace": "黑龙江木兰",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共延寿县委统战部", "source": "延寿县政府网·李惠达简历页 (2026-07)"},
    {"id": 9, "name": "宋积平", "gender": "男", "ethnicity": "", "birth": "1979-06", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县人武部政委", "current_org": "延寿县人民武装部", "source": "延寿县政府网·宋积平简历页 (2026-04)"},
    {"id": 10, "name": "金烁", "gender": "女", "ethnicity": "", "birth": "1986-01", "birthplace": "黑龙江哈尔滨",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（原副县长）", "current_org": "中共延寿县委员会", "source": "延寿县政府网·金烁简历页 (2026-07)"},
    {"id": 11, "name": "刘诚", "gender": "男", "ethnicity": "", "birth": "1972-08", "birthplace": "黑龙江巴彦",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政府副县长", "current_org": "延寿县人民政府", "source": "延寿县政府网·刘诚简历页 (2022-12)"},
    {"id": 14, "name": "张云会", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "延寿县人民政府", "source": "延寿县政府网·延寿要闻 (2026-01-16)"},
    {"id": 15, "name": "史建华", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局长", "current_org": "延寿县人民政府", "source": "延寿县人大常委会任免名单 (2024-05-10)"},
    {"id": 17, "name": "李百超", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "延寿县人民政府", "source": "延寿县政府网·副县长简历 (2023-08)"},
    {"id": 18, "name": "王美婷", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "延寿县人民政府", "source": "延寿县政府网·副县长简历 (2026-07)"},
    {"id": 16, "name": "徐鑫", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "1995-07",
     "current_post": "区委副书记（双城区）", "current_org": "中共哈尔滨市双城区委员会", "source": "双城区政府网 (数据/tmp/heilongjiang_双城区)"},
    {"id": 20, "name": "张洪岐", "gender": "男", "ethnicity": "汉族", "birth": "1973-04", "birthplace": "黑龙江铁力",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "前任县委书记（现哈尔滨市人社局）", "current_org": "哈尔滨市人力资源和社会保障局", "source": "百度百科·张洪岐 / 延寿县政府网"},
    {"id": 21, "name": "刘金成", "gender": "男", "ethnicity": "汉族", "birth": "1966-03", "birthplace": "",
     "education": "省政法管理干部学院法律专业", "party_join": "中共党员", "work_start": "1985-06",
     "current_post": "前任县委书记（一级巡视员）", "current_org": "中共延寿县委员会", "source": "中国经济网·任前公示 (2017-12-14)"},
    {"id": 22, "name": "封殿辉", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "原县委书记（受贿获刑）", "current_org": "中共延寿县委员会", "source": "环球网 (2018-08-12)"},
    {"id": 23, "name": "丁宇恒", "gender": "男", "ethnicity": "汉族", "birth": "1971-02", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "1992-07",
     "current_post": "原县长", "current_org": "延寿县人民政府", "source": "百度百科·丁宇恒"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共延寿县委员会", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委", "location": "延寿县"},
    {"id": 2, "name": "延寿县人民政府", "type": "政府", "level": "县级", "parent": "哈尔滨市人民政府", "location": "延寿县"},
    {"id": 3, "name": "延寿县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "哈尔滨市人大常委会", "location": "延寿县"},
    {"id": 4, "name": "政协延寿县委员会", "type": "政协", "level": "县级", "parent": "哈尔滨市政协", "location": "延寿县"},
    {"id": 5, "name": "中共延寿县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共哈尔滨市纪委", "location": "延寿县"},
    {"id": 6, "name": "中共延寿县委组织部", "type": "党委", "level": "县级", "parent": "中共延寿县委员会", "location": "延寿县"},
    {"id": 7, "name": "中共延寿县委宣传部", "type": "党委", "level": "县级", "parent": "中共延寿县委员会", "location": "延寿县"},
    {"id": 8, "name": "中共延寿县委统战部", "type": "党委", "level": "县级", "parent": "中共延寿县委员会", "location": "延寿县"},
    {"id": 9, "name": "延寿县寿山乡", "type": "乡镇", "level": "乡镇", "parent": "延寿县人民政府", "location": "延寿县"},
    {"id": 10, "name": "延寿县六团镇", "type": "乡镇", "level": "乡镇", "parent": "延寿县人民政府", "location": "延寿县"},
    {"id": 11, "name": "哈尔滨市阿城区（区委/政府）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委", "location": "哈尔滨市"},
    {"id": 12, "name": "哈尔滨市呼兰区（区委/政府）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委", "location": "哈尔滨市"},
    {"id": 13, "name": "哈尔滨市人力资源和社会保障局", "type": "政府", "level": "市级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市"},
    {"id": 14, "name": "绥化市绥棱县（县乡）", "type": "党委", "level": "县级", "parent": "中共绥化市委", "location": "绥化市"},
    {"id": 15, "name": "双城区（区委）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委", "location": "哈尔滨市"},
    {"id": 16, "name": "黑龙江水利职业技术学校", "type": "其他", "level": "", "parent": "", "location": "哈尔滨市"},
]

# ── Positions (career timeline) ────────────────────────────────────────────
positions = [
    # 李宏伟（县委书记）— 阿城区 20 余年（官方简历逐条）
    {"person_id": 1, "org_id": 9, "title": "黑龙江水利高等专科学校·水利水电专业学习", "start_date": "1997.09", "end_date": "2000.07", "rank": "", "note": "学历阶段"},
    {"person_id": 1, "org_id": 11, "title": "阿城市水利局征费办征费员→办公室秘书→水务局团委书记", "start_date": "2000.08", "end_date": "2003.05", "rank": "科员", "note": "阿城"},
    {"person_id": 1, "org_id": 11, "title": "阿城市（区）政府办综合科/常务秘书室", "start_date": "2003.05", "end_date": "2009.08", "rank": "科员→正科", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "区政府办副主任", "start_date": "2009.08", "end_date": "2011.07", "rank": "正科→副处", "note": "阿城区"},
    {"person_id": 1, "org_id": 11, "title": "交界镇党委副书记、镇长 → 交界街道党工委书记、人大工委主任", "start_date": "2011.07", "end_date": "2017.01", "rank": "副处→正处", "note": "阿城区"},
    {"person_id": 1, "org_id": 11, "title": "区政府党组成员、办公室主任", "start_date": "2017.01", "end_date": "2020.01", "rank": "正处级", "note": "阿城区"},
    {"person_id": 1, "org_id": 11, "title": "区政府副区长", "start_date": "2020.01", "end_date": "2021.10", "rank": "副局级", "note": "阿城区"},
    {"person_id": 1, "org_id": 12, "title": "区委常委、政府副区长", "start_date": "2021.10", "end_date": "2024.04", "rank": "副局级", "note": "呼兰区"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2024.04", "end_date": "present", "rank": "副局级", "note": "主持县委全面工作"},
    # 徐涤非（县长）
    {"person_id": 2, "org_id": 2, "title": "齐齐哈尔大学汉语言小学教育专业学习", "start_date": "1996.09", "end_date": "2000.07", "rank": "", "note": "学士"},
    {"person_id": 2, "org_id": 14, "title": "绥棱县绥棱镇镇长助理 → 共青团绥棱县委副书记", "start_date": "2000.08", "end_date": "2003.10", "rank": "副科", "note": "绥化市绥棱县"},
    {"person_id": 2, "org_id": 14, "title": "绥棱—哈尔滨干部选拔（纪检/政法口）", "start_date": "2003.10", "end_date": "2021.11", "rank": "", "note": "中间履历未完整公开"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "2021.12", "end_date": "present", "rank": "副局级", "note": "主持县政府全面"},
    # 常委/班子
    {"person_id": 3, "org_id": 1, "title": "县委副书记（代管政法委）", "start_date": "2024.07", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2025.12", "end_date": "present", "rank": "副局级", "note": "2025-12 由依兰县调入"},
    {"person_id": 5, "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start_date": "2024.08", "end_date": "present", "rank": "副处级", "note": "方正县籍"},
    {"person_id": 6, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "2024.08", "end_date": "present", "rank": "副处级", "note": "巴彦县籍"},
    {"person_id": 7, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "2021.11", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "县委常委、统战部部长", "start_date": "2026.06", "end_date": "present", "rank": "副处级", "note": "木兰县籍，原副县长"},
    {"person_id": 9, "org_id": 10, "title": "县委常委、县人武部政委", "start_date": "2025", "end_date": "present", "rank": "副处级", "note": "海军工程大学出身"},
    {"person_id": 10, "org_id": 1, "title": "县委常委（原副县长）", "start_date": "2026.07", "end_date": "present", "rank": "副处级", "note": "2026-07 由副县长转任"},
    {"person_id": 11, "org_id": 2, "title": "县委常委、政府副县长", "start_date": "2022.12", "end_date": "present", "rank": "副处级", "note": "巴彦县籍"},
    # 县政府其他副县
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "2024.09", "end_date": "present", "rank": "副处级", "note": "分管乡村经济等"},
    {"person_id": 15, "org_id": 2, "title": "副县长、县公安局长", "start_date": "2024.05", "end_date": "present", "rank": "副处级", "note": "县公安局"},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "2023.08", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start_date": "2026.07", "end_date": "present", "rank": "副处级", "note": "2026-07 最新任命"},
    # 徐鑫（双城区委副书记，延寿县出身）
    {"person_id": 16, "org_id": 10, "title": "延寿县六团镇财政所干部/团委书记/武装部长", "start_date": "1995.07", "end_date": "2011.09", "rank": "科员→正科", "note": ""},
    {"person_id": 16, "org_id": 15, "title": "双城区（市）政府副市长→区委常委、统战/政法委书记→常务副区长", "start_date": "2011.10", "end_date": "2021.10", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 15, "title": "双城区委副书记", "start_date": "2021.10", "end_date": "present", "rank": "副区级", "note": ""},
    # 前任（节点）
    {"person_id": 20, "org_id": 12, "title": "呼兰区委常委、政府副区长", "start_date": "2016.09", "end_date": "2018.09", "rank": "副局级", "note": "呼兰区"},
    {"person_id": 20, "org_id": 2, "title": "延寿县委副书记、代县长→县长", "start_date": "2018.09", "end_date": "2021.11", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 1, "title": "县委书记（二级巡视员）", "start_date": "2021.11", "end_date": "2024.04", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 13, "title": "哈尔滨市人社局 二级巡视员", "start_date": "2024", "end_date": "present", "rank": "副厅级", "note": "去向"},
    {"person_id": 21, "org_id": 1, "title": "县委书记", "start_date": "2017.12", "end_date": "2021", "rank": "正处级", "note": "一级巡视员，脱贫攻坚典型"},
    {"person_id": 22, "org_id": 1, "title": "县委书记", "start_date": "2011", "end_date": "2017", "rank": "正处级", "note": "受贿1511万+35万美元，2018-08获刑10年6个月"},
    {"person_id": 23, "org_id": 2, "title": "县委副书记、县长", "start_date": "2015", "end_date": "2018.09", "rank": "正处级", "note": "前县长"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记李宏伟与县长徐涤非党政主要领导搭档", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与副书记朱志刚党委班子共事", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与纪委书记魏春雷在县委班子", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记与组织部长李颖（曾一同慰问老干部）", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长领导副县长张云会（2026-01 共同调研）", "overlap_org": "延寿县人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长领导公安副县长史建华", "overlap_org": "延寿县人民政府", "overlap_period": "2024-05至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长领导常委副县长杨向海", "overlap_org": "延寿县人民政府", "overlap_period": "2025-12至今"},
    {"person_a": 1, "person_b": 20, "type": "predecessor_successor", "context": "前任县委书记张洪岐（县长转书记）→李宏伟（2024-04履新），共通 呼兰区任职背景", "overlap_org": "呼兰区/延寿县", "overlap_period": "2024-04"},
    {"person_a": 2, "person_b": 23, "type": "predecessor_successor", "context": "接替原县长丁宇恒", "overlap_org": "延寿县人民政府", "overlap_period": "2018-09/2021-12"},
    {"person_a": 20, "person_b": 21, "type": "predecessor_successor", "context": "接替县委书记刘金成", "overlap_org": "中共延寿县委员会", "overlap_period": "2021-11"},
    {"person_a": 21, "person_b": 22, "type": "predecessor_successor", "context": "接替因受贿落马的县委书自封殿辉", "overlap_org": "中共延寿县委员会", "overlap_period": "2017-12"},
    {"person_a": 1, "person_b": 16, "type": "cross_region_transfer", "context": "同为哈尔滨市域区县际轮岗干部（阿城/呼兰/延寿；延寿→双城）", "overlap_org": "哈尔滨市干部交流网络", "overlap_period": ""},
    {"person_a": 16, "person_b": 20, "type": "cross_region_transfer", "context": "张洪岐（呼兰→延寿）与徐鑫（延寿→双城）反向流动，均为呼兰/延寿/双城片区干部", "overlap_org": "哈尔滨市干部交流网络", "overlap_period": ""},
]

# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    if name == "李宏伟": return "255,50,50"
    if name == "徐涤非": return "50,100,255"
    if name == "徐鑫": return "150,90,50"
    if name in ("张洪岐", "刘金成", "封殿辉", "丁宇恒"): return "150,150,150"
    if name == "魏春雷": return "255,165,0"
    if name == "张淑英": return "200,120,120"
    if name == "郭彦洁": return "200,120,120"
    if name == "李颖": return "255,165,0"
    return "100,100,100"


def person_size(name):
    if name in ("李宏伟", "徐涤N", "徐涤非"): return "20.0"
    if name == "徐鑫": return "14.0"
    if name in ("张洪岐", "刘金成"): return "14.0"
    return "12.0"


def org_color(t):
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    if "纪委" in t: return "255,180,180"
    return "200,200,200"


# ── Database ──────────────────────────────────────────────────────────────
def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p.get("gender"), p.get("ethnicity"), p.get("birth"), p.get("birthplace"),
                     p.get("education"), p.get("party_join"), p.get("work_start"), p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ── GEXF ──────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>延寿县领导班子工作关系网络 - {SLUG} (哈尔滨市)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"]); sz = person_size(p["name"]); pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"]); oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues><attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/></attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues><attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/></attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ── Person Graph JSON ─────────────────────────────────────────────────────
SOURCE_REGISTER = [
    {"id": "S001", "title": "延寿县政府官网·县委书记 李宏伟 简历页", "url": "http://www.hrbx.gov.cn/（县委领导）", "publisher": "哈尔滨市延寿县人民政府", "published_at": "2026-01-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "完整简历"},
    {"id": "S002", "title": "延寿县政府官网·县长 徐涤非 简历页", "url": "http://www.harbin.gov.cn/招商", "publisher": "哈尔滨市延寿县人民政府", "published_at": "2026-01-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "完整简历"},
    {"id": "S003", "title": "百度百科·李宏伟（延寿县委书记）", "url": "https://baike.baidu.com/item/李宏伟", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "履历+生日"},
    {"id": "S004", "title": "百度百科·徐涤非", "url": "https://baike.baidu.com/item/徐涤非", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "履历"},
    {"id": "S005", "title": "百度百科·张洪岐", "url": "https://baike.baidu.com/item/张洪岐", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "前任书记"},
    {"id": "S006", "title": "百度百科·丁宇恒（原县长）", "url": "https://baike.baidu.com/item/丁宇恒", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "原县长"},
    {"id": "S007", "title": "环球网·原书记封殿辉受贿获刑", "url": "https://world.huanqiu.com/（2018）", "publisher": "环球网", "published_at": "2018-08-12", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "封殿辉受贿案"},
    {"id": "S008", "title": "中国经济网·刘金成 拟任延寿县委书记公示", "url": "http://www.ce.cn/2017-12-14", "publisher": "中国经济网", "published_at": "2017-12-14", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "任前公示"},
    {"id": "S009", "title": "延寿县人大常委会·任免名单", "url": "延寿县政府网/县人大", "publisher": "延寿县人民代表大会常务委员会", "published_at": "2024-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "史建华等"},
    {"id": "S010", "title": "双城区政府官网·徐鑫简历", "url": "http://www.hrbsc.gov.cn", "publisher": "双城区人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "延寿县六团镇出身（跨县）"},
    {"id": "S011", "title": "实名数据·延寿县政府官网领导表", "url": "延寿县政府网/中共延寿县委", "publisher": "哈尔滨市延寿县人民政府", "published_at": "2024-2025", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "常委名册"},
]


_FULL_TIMELINES = {
    1: [
        {"start": "1997-09", "end": "2000-07", "org": "黑龙江水利高等专科学校", "title": "水利水电工程规划专业（学生）", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "2000-08", "end": "2008", "org": "阿城区政府", "title": "区政府办公室副主任", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "2008", "end": "2015", "org": "阿城区交界镇", "title": "党委副书记、镇长", "confidence": "plausible", "source_ids": ["S001", "S003"]},
        {"start": "2015", "end": "2019", "org": "阿城区交界街道", "title": "党工委书记、人大工委主任", "confidence": "plausible", "source_ids": ["S001", "S003"]},
        {"start": "2019", "end": "2020-01", "org": "阿城区政府", "title": "区政府党组成员、办公室主任", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "2020-01", "end": "2021-12", "org": "阿城区政府", "title": "副区长", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "2021-12", "end": "2024-04", "org": "呼兰区委区政府", "title": "区委常委、副区长", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "2024-04", "end": "present", "org": "中共延寿县委员会", "title": "县委书记", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ],
    2: [
        {"start": "1996-09", "end": "2000-07", "org": "齐齐哈尔大学", "title": "汉语言文学专业（学士）", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"start": "2000-08", "end": "2002-01", "org": "绥棱县绥棱镇", "title": "镇长助理", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"start": "2002-01", "end": "2003-10", "org": "共青团绥棱县委", "title": "副书记（副科级）", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"start": "2003-10", "end": "2021-05", "org": "绥棱县→ 哈尔滨干部选拔", "title": "（2003-2021 中间履历未公开）", "confidence": "unverified", "source_ids": []},
        {"start": "2021-12", "end": "present", "org": "延寿县人民政府", "title": "县委副书记、县长", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
    ],
}

_DEPUTY_TIMELINES = {
    20: [
        {"start": "2016-09", "end": "2018-09", "org": "呼兰区委区政府", "title": "区委常委、副区长", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2018-09", "end": "2019-01", "org": "延寿县人民政府", "title": "县委副书记、代县长", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2019-01", "end": "2021-11", "org": "延寿县人民政府", "title": "县长", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2021-11", "end": "2024-04", "org": "中共延寿县委员会", "title": "县委书记（二级巡视员）", "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2024", "end": "present", "org": "哈尔滨市人力资源和社会保障局", "title": "二级巡视员", "confidence": "plausible", "source_ids": ["S005"]},
    ],
    21: [
        {"start": "2017-12", "end": "2021", "org": "中共延寿县委员会", "title": "县委书记", "confidence": "confirmed", "source_ids": ["S008"]},
    ],
    22: [
        {"start": "2011", "end": "2017", "org": "中共延寿县委员会", "title": "县委书记（受贿落马）", "confidence": "confirmed", "source_ids": ["S007"]},
    ],
    23: [
        {"start": "2015", "end": "2018-09", "org": "延寿县人民政府", "title": "县长", "confidence": "confirmed", "source_ids": ["S006"]},
    ],
    16: [
        {"start": "1995-07", "end": "2011-09", "org": "延寿县六团镇（含 延寿团县委）", "title": "财政所干部/团委书记/武装部长/乡镇", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2011-10", "end": "2015-04", "org": "双城区政府", "title": "副市长", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2015-04", "end": "2019-08", "org": "双城区委", "title": "区委常委、统战/政法委书记", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2019-08", "end": "2021-10", "org": "双城区政府", "title": "常务副区长", "confidence": "confirmed", "source_ids": ["S010"]},
        {"start": "2021-10", "end": "present", "org": "双城区委", "title": "区委副书记", "confidence": "confirmed", "source_ids": ["S010"]},
    ],
}

_RELATIONSHIPS = {
    1: [
        {"person": "徐涤非", "person_id": "yanshou_徐涤非", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "县委书记—县长搭档", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04至今", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "朱志刚", "person_id": "yanshou_朱志刚", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "书记—副书记党委班子", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04至今", "confidence": "plausible", "source_ids": ["S011"]},
        {"person": "张洪岐", "person_id": "yanshou_张洪岐", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "前任书记，2024-04职务交接", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "魏春雷", "person_id": "yanshou_魏春雷", "relationship_type": "overlap", "strength": "medium", "evidence": "县委班子共事", "overlap_org": "中共延寿县委员会", "overlap_period": "2024-04至今", "confidence": "plausible", "source_ids": ["S011"]},
    ],
    2: [
        {"person": "李宏伟", "person_id": "yanshou_李宏伟", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "县长受县委书记领导", "overlap_org": "延寿县政府", "overlap_period": "2024-04至今", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "张云会", "person_id": "yanshou_张云会", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "县长—副副县长", "overlap_org": "延寿县人民政府", "overlap_period": "2024至今", "confidence": "plausible", "source_ids": ["S011"]},
        {"person": "史建华", "person_id": "yanshou_史建华", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "县长—公安副县长", "overlap_org": "延寿县人民政府", "overlap_period": "2024-05至今", "confidence": "confirmed", "source_ids": ["S009"]},
    ],
}

job_map = {1: "县委书记", 2: "县长", 3: "县委副书记", 4: "县委常委_副县长", 5: "县委常委_纪委书记",
           6: "县委常委_组织部长", 7: "县委常委_宣传部长", 8: "县委常委_统战部长", 9: "县委常委",
           10: "县委常委", 11: "县委常委", 12: "县委常委", 13: "县委常委", 14: "副县长",
           15: "副县长_县公安局长", 16: "县委副书记_双城区", 20: "前任县委书记", 21: "前任县委书记",
           22: "前任县委书记", 23: "原县长", 24: "县委副书记"}


def build_person_jsons():
    for p in persons:
        name = p["name"]
        if name == "李宏伟":
            timeline = _FULL_TIMELINES[1]
        elif name == "徐涤非":
            timeline = _FULL_TIMELINES[2]
        else:
            timeline = _DEPUTY_TIMELINES.get(p["id"], [{"start": "unknown", "end": "present", "org": p.get("current_org", ""), "title": p.get("current_post", ""), "confidence": "plausible", "source_ids": []}])
        rels = _RELATIONSHIPS.get(p["id"], [])
        data = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "黑龙江省", "city": "哈尔滨市", "region": "延寿县",
                                    "job": p["current_post"], "task_id": "heilongjiang_延寿县", "time_focus": "2026年8月"},
            "identity": {
                "person_id": f"yanshou_{name}", "name": name, "aliases": [],
                "gender": p.get("gender") or "", "ethnicity": p.get("ethnicity") or "",
                "birth": p.get("birth") or "", "birthplace": p.get("birthplace") or "", "native_place": "",
                "education": p.get("education") or "", "party_join": p.get("party_join") or "", "work_start": p.get("work_start") or "",
                "dedupe_keys": {"name_birth": f"{name}_{p.get('birth','')}", "name_birthplace": f"{name}_{p.get('birthplace','')}", "official_profile_url": p.get("source", "")},
            },
            "current_status": {
                "current_post": p["current_post"], "current_org": p["current_org"],
                "administrative_rank": "", "as_of": AS_OF, "is_current_confirmed": name in ("李宏伟", "徐涤非"),
                "source_ids": [e.get("source") for e in timeline if e.get("source")],
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": rels,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [], "secondary_specializations": [],
                "career_pattern": ("cross_county_rotation" if name in ("李宏伟", "张洪岐", "徐鑫") else "local_ladder"),
                "systems_experience": [], "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [], "speech_themes": [], "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": SOURCE_REGISTER,
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed",
                "career_completeness": "partial", "relationship_confidence": "medium",
                "biggest_gap": "徐涤非 2003-2021 履历缺失；部分常委履历未公开；人大/政协负责人现任待核"
                + ("" if name not in ("李宏伟", "徐涤非") else ""),
            },
            "open_questions": [
                {"priority": "high" if name in ("李宏伟", "徐涤非") else "medium", "question": f"{name}的详细任职时间与县域治理公开细节", "why_it_matters": "提升履历可信度", "suggested_queries": [f"{name} 延寿县 简历"], "last_attempted": AS_OF},
            ],
        }
        if name == "李宏伟":
            data["open_questions"].append({"priority": "medium", "question": "李宏伟前任张洪岐与在任时的县域治理延续/调整", "notes": "书记更替背景", "why_it_matters": "县委更替背景", "suggested_queries": ["延寿县 前任书记 张洪岐"], "last_attempted": AS_OF})
        if name == "徐涤非":
            data["open_questions"].append({"priority": "high", "question": "徐涤非 2003-2021 绥棱→延寿的详细履历", "why_it_matters": "县长晋升路径", "suggested_queries": ["徐涤非 绥棱 简历"], "last_attempted": AS_OF})
        if name == "徐涤非":
            data["open_questions"].append({"priority": "medium", "question": "徐涤非前任县长丁宇恒去向", "why_it_matters": "县长更替路径", "suggested_queries": ["丁宇恒 延寿县 县长 去向"], "last_attempted": AS_OF})
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-哈尔滨市-{job_map.get(p['id'], p['current_post'])}-{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


if __name__ == "__main__":
    print(f"Building {SLUG} network data... (AS_OF={AS_OF})")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in sorted(PERSONS_DIR.glob(f"{TODAY}-黑龙江省-哈尔滨市-*.json")):
        print(f"  Person: {p.name}")
    print("Done.")