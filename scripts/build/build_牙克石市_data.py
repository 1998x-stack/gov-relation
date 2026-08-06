#!/usr/bin/env python3
"""牙克石市领导班子工作关系网络生成脚本.

研究对象：内蒙古自治区呼伦贝尔市牙克石市（县级市）市委书记、市长及
市委、政府、人大、政协领导班子成员。

数据时间锚点：截至 2026-08-06（模拟环境日期）。
权威一手来源（confirmed）：
- 牙克石市人民政府门户「领导之窗」(www.yks.gov.cn/Leader/) 各领导个人简历页
- 中国共产党牙克石市第十六次代表大会胜利闭幕（2026-07-31，News/1446463）
- 十六届市委第一次全体会议公报（2026-07-31，News/1446458，选举产生的十六届市委常务委员会）
- 牙克石市第十六届人大常委会第三十八次会议（2026-08-05，News/1447346，任命代理市长/代理监委主任等）
- 中国共产党牙克石市第十六次代表大会上的报告（2026-07-30，栾永刚，News/1446560）

本期人事变动（2026-08-05 人大常委会第三十八次会议）：
- 李忠伟 由市委常委、市政府党组副书记、副市长 任 代理市长
- 姚家义 兼任市政府副市长（仍任市委组织部部长）
- 乔杰 任市监委副主任、代理主任（纪委班子成员，达斡尔族）
- 接受 杜晓光 辞去副市长，接受 石伟 辞去监委主任

说明：市委书记 栾永刚 于 2020 年代系中共牙克石市第十五届至十六届委员会书记（第十五届委员会报告由
其代表市委作出），十六届一次全会续任书记。市长岗位处于换届过渡期，李忠伟为代理市长（暂未选举为正式市长）。
个人早期履历（工作起始年份、前任职务、跨县区流转）公开资料有限，已明确标注于 open_questions。
"""

from __future__ import annotations

import sqlite3  # 标准库（数据库落库经由 gov_relation.runner）
import sys
from pathlib import Path

# 项目根目录（兼容 data/tmp/<task_id>/、scripts/build/、仓库根 三种位置）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = next((p for p in _HERE.parents if (p / "gov_relation").is_dir()), _HERE)
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

SLUG = "牙克石市"
DB_PATH = _HERE / "牙克石市_network.db"
GEXF_PATH = _HERE / "牙克石市_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
# 官方「领导之窗」简历确认身份；民族/出生/学历来自官方个人简介页
PERSONS = [
    # 1 现任市委书记
    {"id": 1, "name": "栾永刚", "gender": "男", "ethnicity": "汉族", "birth": "1971-03",
     "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委书记", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/Leader/show/45/88.html"},
    # 2 代理市长 / 市委副书记
    {"id": 2, "name": "李忠伟", "gender": "男", "ethnicity": "汉族", "birth": "1981-08",
     "birthplace": "", "education": "大学学历，管理学学士",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市代理市长、市委副书记", "current_org": "牙克石市人民政府",
     "source": "https://www.yks.gov.cn/Leader/show/45/1051.html"},
    # 3 市委副书记、政法委书记
    {"id": 3, "name": "杨荣彬", "gender": "男", "ethnicity": "汉族", "birth": "1984-03",
     "birthplace": "", "education": "大学学历，公共管理硕士",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委副书记、政法委书记", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/Leader/show/45/985.html"},
    # 4 市委常委、统战部部长
    {"id": 4, "name": "陈旭呈", "gender": "男", "ethnicity": "汉族", "birth": "1973-02",
     "birthplace": "", "education": "农学学士",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委常委、统战部部长", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/Leader/show/45/941.html"},
    # 5 市委常委、组织部部长（兼副市长）
    {"id": 5, "name": "姚家义", "gender": "男", "ethnicity": "回族", "birth": "1979-12",
     "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委常委、组织部部长、副市长", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/Leader/show/45/1003.html"},
    # 6 市委常委、市委办公室主任
    {"id": 6, "name": "晋国军", "gender": "男", "ethnicity": "汉族", "birth": "1978-05",
     "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委常委、市委办公室主任", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/Leader/show/45/939.html"},
    # 7 市委常委、纪委书记、监委主任（代理主任 乔杰 任命后，石伟不再兼监委主任）
    {"id": 7, "name": "石伟", "gender": "女", "ethnicity": "蒙古族", "birth": "1984-08",
     "birthplace": "", "education": "研究生学历，理学硕士",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委常委、纪委书记", "current_org": "中国共产党牙克石市纪律检查委员会",
     "source": "https://www.yks.gov.cn/Leader/show/45/986.html"},
    # 8 市委常委、监委代理主任（达斡尔族，2026-08-05 任命；纪委新一届书记）
    {"id": 8, "name": "乔杰", "gender": "男", "ethnicity": "达斡尔族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委常委、纪委书记、监委代理主任", "current_org": "中共牙克石市纪律检查委员会",
     "source": "https://www.yks.gov.cn/News/show/1446458.html"},
    # 9 市委常委、宣传部部长
    {"id": 9, "name": "吴迪", "gender": "女", "ethnicity": "蒙古族", "birth": "1987-08",
     "birthplace": "", "education": "大学学历，文学学士",
     "party_join": "2007-11", "work_start": "2009-09",
     "current_post": "牙克石市委常委、宣传部部长", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/Leader/show/45/987.html"},
    # 10 市委常委、副市长
    {"id": 10, "name": "许永哲", "gender": "男", "ethnicity": "汉族", "birth": "1987-01",
     "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委常委、副市长", "current_org": "牙克石市人民政府",
     "source": "https://www.yks.gov.cn/Leader/show/45/1041.html"},
    # 11 市人大常委会主任
    {"id": 11, "name": "高勇", "gender": "男", "ethnicity": "汉族", "birth": "1967-02",
     "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市人大常委会主任", "current_org": "牙克石市人民代表大会常务委员会",
     "source": "https://www.yks.gov.cn/Leader/show/44/115.html"},
    # 12 市政协主席
    {"id": 12, "name": "李继忠", "gender": "男", "ethnicity": "汉族", "birth": "1968-06",
     "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市政协主席", "current_org": "中国人民政治协商会议牙克石市委员会",
     "source": "https://www.yks.gov.cn/Leader/show/42/931.html"},
    # 13 副市长
    {"id": 13, "name": "张大亮", "gender": "男", "ethnicity": "蒙古族", "birth": "1971-09",
     "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市副市长", "current_org": "牙克石市人民政府",
     "source": "https://www.yks.gov.cn/Leader/show/43/936.html"},
    # 14 副市长
    {"id": 14, "name": "杨婧", "gender": "女", "ethnicity": "蒙古族", "birth": "1986-05",
     "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市副市长", "current_org": "牙克石市人民政府",
     "source": "https://www.yks.gov.cn/Leader/show/43/108.html"},
    # 15 副市长
    {"id": 15, "name": "张昕宇", "gender": "男", "ethnicity": "汉族", "birth": "1975-02",
     "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市副市长", "current_org": "牙克石市人民政府",
     "source": "https://www.yks.gov.cn/Leader/show/43/113.html"},
    # 16 副市长
    {"id": 16, "name": "王洪强", "gender": "男", "ethnicity": "回族", "birth": "1980-03",
     "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市副市长", "current_org": "牙克石市人民政府",
     "source": "https://www.yks.gov.cn/Leader/show/43/110.html"},
    # 17 市人大常委会副主任
    {"id": 17, "name": "孙好民", "gender": "男", "ethnicity": "汉族", "birth": "1969-05",
     "birthplace": "", "education": "大学学历，农学学士",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市人大常委会副主任", "current_org": "牙克石市人民代表大会常务委员会",
     "source": "https://www.yks.gov.cn/Leader/show/44/116.html"},
    # 18 市人大常委会副主任（官方岗位）
    {"id": 18, "name": "闫敬东", "gender": "男", "ethnicity": "汉族", "birth": "1968-01",
     "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市人大常委会副主任", "current_org": "牙克石市人民代表大会常务委员会",
     "source": "https://www.yks.gov.cn/Leader/"},
    # 19 市人大常委会副主任
    {"id": 19, "name": "杜利军", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市人大常委会副主任", "current_org": "牙克石市人民代表大会常务委员会",
     "source": "https://www.yks.gov.cn/Leader/"},
    # 20 市人大常委会副主任
    {"id": 20, "name": "包海花", "gender": "女", "ethnicity": "蒙古族", "birth": "1970-02",
     "birthplace": "", "education": "中央党校大学",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市人大常委会副主任", "current_org": "牙克石市人民代表大会常务委员会",
     "source": "https://www.yks.gov.cn/Leader/show/44/120.html"},
    # 21 十六届市委常委（新进常委会，官方未刊个人简历）
    {"id": 21, "name": "高华兵", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委委员（十六届常委会成员）", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/News/show/1446458.html"},
    # 22 十六届市委常委（新进）
    {"id": 22, "name": "王赞杰", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "牙克石市委委员（十六届常委会成员）", "current_org": "中国共产党牙克石市委员会",
     "source": "https://www.yks.gov.cn/News/show/1446458.html"},
    # 23 原副市长（2026-08-05 辞去副市长）
    {"id": 23, "name": "杜晓光", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "（原牙克石市副市长，2026-08-05 辞任）", "current_org": "",
     "source": "https://www.yks.gov.cn/News/show/1447346.html"},
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党牙克石市委员会", "type": "党委", "level": "县级", "parent": "中国共产党呼伦贝尔市委员会", "location": "内蒙古呼伦贝尔牙克石市"},
    {"id": 2, "name": "牙克石市人民政府", "type": "政府", "level": "县级", "parent": "呼伦贝尔市人民政府", "location": "内蒙古呼伦贝尔牙克石市"},
    {"id": 3, "name": "牙克石市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "内蒙古呼伦贝尔牙克石市"},
    {"id": 4, "name": "中国人民政治协商会议牙克石市委员会", "type": "政协", "level": "县级", "parent": "", "location": "内蒙古呼伦贝尔牙克石市"},
    {"id": 5, "name": "中共牙克石市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中国共产党牙克石市委员会", "location": "内蒙古呼伦贝尔牙克石市"},
    {"id": 6, "name": "牙克石市监察委员会", "type": "党委", "level": "县级", "parent": "", "location": "内蒙古呼伦贝尔牙克石市"},
    {"id": 7, "name": "中国共产党呼伦贝尔市委员会", "type": "党委", "level": "地级", "parent": "", "location": "内蒙古呼伦贝尔"},
    {"id": 8, "name": "呼伦贝尔市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "内蒙古呼伦贝尔"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-07-31", "end_date": "present", "rank": "正处级", "note": "现任十六届市委（十六次党代会续任书记）；此前即任十五届市委书记，2026-07-31十六届一次全会续选为书记"},
    {"person_id": 2, "org_id": 2, "title": "代理市长", "start_date": "2026-08-05", "end_date": "present", "rank": "正处级", "note": "2026-08-05市人大常委会决定任命为代理市长；此前任市委常委、市政府党组书记、常务副市长，十六届党代会为市长候选人"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2026-08-01", "end_date": "present", "rank": "副处级", "note": "十六届市委副书记"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "2026-08-01", "end_date": "present", "rank": "副处级", "note": "十六届市委副书记"},
    {"person_id": 4, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "十六届市委常委"},
    {"person_id": 5, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "十六届市委常委；兼老干部局局长、市直机关工委书记"},
    {"person_id": 5, "org_id": 2, "title": "副市长（兼）", "start_date": "2026-08-05", "end_date": "present", "rank": "副处级", "note": "2026-08-05人大常委会任免为副市长"},
    {"person_id": 6, "org_id": 1, "title": "市委常委、市委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "十六届市委常委"},
    {"person_id": 7, "org_id": 5, "title": "市委常委、纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "十六届市委委员；2026-08-05辞监委主任职务，仍任纪委书记、市委常委"},
    {"person_id": 8, "org_id": 5, "title": "市委常委、纪委书记", "start_date": "2026-08-01", "end_date": "present", "rank": "副处级", "note": "十六届纪委书记（选举产生），十六届一次全会通过纪委领导名单；2026-08-05任监委代理主任"},
    {"person_id": 8, "org_id": 6, "title": "监察委员会代理主任", "start_date": "2026-08-05", "end_date": "present", "rank": "副处级", "note": "2026-08-05人大常委会任命"},
    {"person_id": 9, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "十六届市委常委；2009-09参加工作，2007-11入党"},
    {"person_id": 10, "org_id": 1, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "十六届市委常委，市政府党组成员"},
    {"person_id": 11, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "市人大常委会党组书记"},
    {"person_id": 12, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "市政协党组书记"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "市政府党组成员"},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "市政府党组成员"},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "市政府党组成员"},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "出生、民族待查"},
    {"person_id": 20, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 1, "title": "市委委员（十六届常委会成员）", "start_date": "2026-07-31", "end_date": "present", "rank": "", "note": "十六届市委常委会委员（官方公报）"},
    {"person_id": 22, "org_id": 1, "title": "市委委员（十六届常委会成员）", "start_date": "2026-07-31", "end_date": "present", "rank": "", "note": "十六届市委常委会委员（官方公报）"},
    {"person_id": 23, "org_id": 2, "title": "副市长（前任，2026-08-05辞任）", "start_date": "", "end_date": "2026-08-05", "rank": "副处级", "note": "因工作变动本人申请辞去副市长职务，2026-08-05人大常委会接受"},
]

# ── Relationships (person <-> person) ─────────────────────────────────────
RELATIONSHIPS = [
    # 书记-市长搭档
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "栾永刚（市委书记）与李忠伟（代理市长）组成党政领导班子搭档，共事于牙克石市委/市政府", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "2026-08至今"},
    # 李忠伟-杨荣彬：副书记共事
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "李忠伟与杨荣彬同为十六届市委副书记", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "2026-08至今"},
    # 乔杰-石伟：纪委职务接替（前任书记/继任）
    {"person_a": 8, "person_b": 7, "type": "前任后任", "context": "乔杰接任纪委书记、监委代理主任，接替辞去监委主任的石伟（石伟仍任市委常委、纪委书记）", "overlap_org": "中共牙克石市纪律检查委员会", "overlap_period": "2026-08"},
    # 李忠伟-杜勃光：政府班子调动（代理市长接替）
    {"person_a": 2, "person_b": 23, "type": "前后任", "context": "杜晓光辞任副市长（2026-08-05），李忠伟任代理市长，市政府班子交替", "overlap_org": "牙克石市人民政府", "overlap_period": "2026-08"},
    # 书记- 各常委 上下级
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记与市委副书记、政法委书记共朔，市委班子主要成员", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记与统战部长同届市委班子", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记与组织部长同届市委班子（组织部长兼副市长）", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "书记与宣传部长同届市委班子", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记与市委办主任", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "书记与常委、副市长", "overlap_org": "中国共产党牙克石市委员会", "overlap_period": "present"},
    # 代理市长-政府班子
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "代理市长与副市长同届政府班子", "overlap_org": "牙克石市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "代理市长与副市长", "overlap_org": "牙克石市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "代理市长与副市长", "overlap_org": "牙克石市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "代理市长与副市长", "overlap_org": "牙克石市人民政府", "overlap_period": "present"},
    # 四套班子
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记与人大主任同届党组", "overlap_org": "", "overlap_period": "present"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "书记与政协主席同届", "overlap_org": "", "overlap_period": "present"},
]

# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"Building 牙克石市 leadership network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    for p in [DB_PATH, GEXF_PATH]:
        if p.exists():
            print(f"  OK {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  MISSING {p.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()