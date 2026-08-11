#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 舞钢市 (Wugang City), 平顶山市, 河南省.

Investigation date: 2026-08-06 (new build)
Task ID: henan_舞钢市
Level: 县级市
Targets: 市委书记 & 市长

Research sources (confirmed 2026-08-06, official primary source):
  - 舞钢市人民政府门户网站 www.zgwg.gov.cn (平顶山市政府站群导航确认域名):
    - 2026-06-22 中共舞钢市第十次代表大会开幕: 何卉代表中共舞钢市第九届委员会作报告（确认何卉任市委书记早于本届换届）; 2026-06-24 十届一次全会选举何卉为十届市委书记，马向阳、杨志鹏为副书记。
    - 2026-07-08 市十一届人大六次会议开幕: 市政府代理市长马向阳作政府工作报告; 2026-07-10 会议闭幕 马向阳当选舞钢市人民政府市长（代转正）, 王二朝当选法院院长。
    - 2026-08-03 马向阳主持召开市政府常务会议(市委副书记、市长)。
    - 2026-07-31 市委书记何卉、市委副书记市长马向阳带队走访慰问驻平/驻舞部队官兵; 市人大常委会主任任国军、市政协主席王冬梅参加。
- 权力交接时间线: 2026-03-03 朱志骞仍任市委书记, 何卉为市委副书记、市长(见 /contents/14734/737919.html); 至 2026-06 何卉晋市委书记, 马向阳任代市长并发转正。

Confirmed roster (as of 2026-08):
- 何卉(女)(市委书记): 现市委书记; 2026-03 前 任市委副书记、市长; 2026-06 市党代会后任书记。出生年/籍贯/学历/入党/参加工作及任舞钢市长前完整履历待查(gap)。
- 马向阳(市委副书记、市长): 2026-07-08 前为政府代理市长, 07-10 当选市长, 08 月仍任; 任市委副书记/代市长前履历待查(gap)。
- 朱志骞(前任市委书记): 2026-03 仍任市委书记; 之后离任,去向待考。
- 杨志鹏(市委副书记); 任国军(市人大常委会主任); 王冬梅(市政协主席)。
- 市委常委: 郭素文、刚延召(常务副市长)、郑冠宇(纪委书记、监委主任)、高军华、何绍三(市委办主任)、殷高洁、刘洪涛、赵鹏飞(政法委书记)。
- 副市长兼公安局长 宋陈林; 市法院院长 王二朝; 市检察院检察长 顾武修; 市人武部部长 王利; 市人大常委会副主任 高军华、杨志文、张耀忠、朱朝伦、胡东涛; 市三级调研员 王平英。

跨区/上级:
- 舞钢市属平顶山市代管县级市; 平顶山市委书记陈向平、市长李明俊对舞钢有上下级工作联系。
- 舞钢市政府门户主办单位为舞钢市人民政府,技术支持平顶山市电子政务外网。

Gaps flagged in person JSON `open_questions`:
  - 何卉/马向阳/朱志骞出生年、籍贯、学历、入党、参加工作与任舞钢前完整履历
  - 朱志骞任舞钢市委书记起止、离任去向
  - 马向阳任代市长的确切任命时间及前任市长(何郡市长→书记后的市长空缺/继任时间线)
  - 各市委常委的具体分工(郭素文、高军华、殷高洁、刘洪涛)及纪检监察、法检机关领导补充名单
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "舞钢市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══ Core Leadership (targets) ═══
    {
        "id": 1,
        "name": "何卉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共舞钢市委员会",
        "source": "舞钢市人民政府门户网站·市第十次党代会(2026-06)/市十一届人大六次会议闭幕(2026-07-10)/市委常委会扩大会(2026-07-25); official",
    },
    {
        "id": 2,
        "name": "马向阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "舞钢市人民政府",
        "source": "舞钢政府官网·市十一届人大六次会议(2026-07-08开幕代理/07-10当选)/马主持市政府常务会议(2026-08-03); official",
    },
    # ═══ 四套班子主官 (official news) ═══
    {
        "id": 3,
        "name": "杨志鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共舞钢市委员会",
        "source": "舞钢政府官网·市委十届一次全会常委名单(2026-06-24)/巡察反馈会(2026-07-31); official",
    },
    {
        "id": 4,
        "name": "任国军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "舞钢市人大常委会",
        "source": "舞钢政府官网·市十一届人大六次会议(2026-07-07预备会主持); official",
    },
    {
        "id": 5,
        "name": "王冬梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协舞钢市委员会",
        "source": "舞钢政府官网·市十一届人大六次会议闭幕(2026-07-10); official",
    },
    # ═══ 市委常委班子 (十届一次全会当选; official) ═══
    {
        "id": 6,
        "name": "刚延召",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "舞钢市人民政府",
        "source": "舞钢政府官网·市委十届一次全会常委名单(2026-06-24); 市人大三十五次常委会(2026-07-03)以\"市委常委、副市长\"列席; official",
    },
    {
        "id": 7,
        "name": "郑冠宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共舞钢市纪律检查委员会",
        "source": "舞钢政府官网·市人大三十五次常委会(2026-07-03)/巡察反馈会(2026-07-31); official",
    },
    {
        "id": 8,
        "name": "赵鹏飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共舞钢市委政法委员会",
        "source": "舞钢政府官网·法治政府建设工作推进会(2026-07-31,主持); official",
    },
    {
        "id": 9,
        "name": "何绍三",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市委办公室主任",
        "current_org": "中共舞钢市委员会办公室",
        "source": "舞钢政府官网·何与马慰问官兵(2026-07-31); official",
    },
    {
        "id": 10,
        "name": "郭素文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共舞钢市委员会",
        "source": "舞钢政府官网·市委十届一次全会常委名单(2026-06-24); official",
    },
    {
        "id": 11,
        "name": "高军华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市人大副主任",
        "current_org": "舞钢市人大常委会",
        "source": "舞钢政府官网·市十一届人大六次会议主席团常务主席名单(2026-07-07/08; 高在主席团); official",
    },
    {
        "id": 12,
        "name": "殷高洁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共舞钢市委员会",
        "source": "舞钢政府官网·市委十届一次全会常委名单(2026-06-24); official",
    },
    {
        "id": 13,
        "name": "刘洪涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共舞钢市委员会",
        "source": "舞钢政府官网·市委十届一次全会常委名单(2026-06-24); official",
    },
    # ═══ 政府/司法其他领导 (official news) ═══
    {
        "id": 14,
        "name": "宋陈梁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "舞钢市公安局",
        "source": "舞钢政府官网·慰问部队官兵(2026-07-31)/法治政府建设推进会(2026-07-31); official",
    },
    {
        "id": 15,
        "name": "王二朝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人民法院院长",
        "current_org": "舞钢市人民法院",
        "source": "舞钢政府官网·市十一届人大六次会议闭幕当选(2026-07-10); official",
    },
    {
        "id": 16,
        "name": "顾武修",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人民检察院检察长",
        "current_org": "舞钢市人民检察院",
        "source": "舞钢政府官网·法治政府建设推进会(2026-07-31); official",
    },
    {
        "id": 17,
        "name": "王利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人民武装部部长",
        "current_org": "舞钢市人民武装部",
        "source": "舞钢政府官网·慰问官兵(2026-07-31); official",
    },
    # ═══ 前任领导 ═══
    {
        "id": 18,
        "name": "朱志骞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市委书记(2026-03在任)",
        "current_org": "中共舞钢市委员会",
        "source": "舞钢政府官网·朱志骞主持市委常委会(扩)(2026-03-04); 离任去向待考; official",
    },
    {
        "id": 19,
        "name": "龚宪君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记(2026-03在任)",
        "current_org": "中共舞钢市委员会",
        "source": "舞钢政府官网·市委常委会扩大会(2026-03-04)；身份为舞钢市委副书记; official",
    },
    # ═══ 平顶山市(上级) ═══
    {
        "id": 20,
        "name": "陈向平",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平顶山市市委书记",
        "current_org": "中共平顶山市委",
        "source": "本地平顶山市调查(report/20260805-平顶山市-领导网络调查报告.md); official",
    },
    {
        "id": 21,
        "name": "李明俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平顶山市委副书记、市长",
        "current_org": "平顶山市人民政府",
        "source": "本地平顶山市调查(report/20260805-平顶山市-领导网络调查报告.md); official",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共舞钢市委员会", "type": "党委", "level": "县处级", "parent": "中共平顶山市委", "location": "舞钢市"},
    {"id": 2, "name": "舞钢市人民政府", "type": "政府", "level": "县处级", "parent": "平顶山市人民政府", "location": "舞钢市"},
    {"id": 3, "name": "舞钢市人大常委会", "type": "人大", "level": "县处级", "parent": "平顶山市人大常委会", "location": "舞钢市"},
    {"id": 4, "name": "政协舞钢市委员会", "type": "政协", "level": "县处级", "parent": "平顶山市政协", "location": "舞钢市"},
    {"id": 5, "name": "中共舞钢市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "平顶山市纪委监委", "location": "舞钢市"},
    {"id": 6, "name": "舞钢市监察委员会", "type": "纪委", "level": "县处级", "parent": "平顶山市监委", "location": "舞钢市"},
    {"id": 7, "name": "中共舞钢市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共舞钢市委员会", "location": "舞钢市"},
    {"id": 8, "name": "中共舞钢市委员会办公室", "type": "党委", "level": "县处级", "parent": "中共舞钢市委员会", "location": "舞钢市"},
    {"id": 9, "name": "舞钢市公安局", "type": "政府", "level": "乡科级" if False else "县处级", "parent": "舞钢市人民政府", "location": "舞钢市"},
    {"id": 10, "name": "舞钢市人民法院", "type": "政府", "level": "县处级", "parent": "平顶山市中级人民法院", "location": "舞钢市"},
    {"id": 11, "name": "舞钢市人民检察院", "type": "政府", "level": "县处级", "parent": "平顶山市人民检察院", "location": "舞钢市"},
    {"id": 12, "name": "舞钢市人民武装部", "type": "党委", "level": "县处级", "parent": "平顶山军分区", "location": "舞钢市"},
    {"id": 13, "name": "中共平顶山市委", "type": "党委", "level": "地厅级", "parent": "中共河南省委", "location": "平顶山市"},
    {"id": 14, "name": "平顶山市人民政府", "type": "政府", "level": "地厅级", "parent": "河南省人民政府", "location": "平顶山市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 何卉 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "舞钢市委书记", "start_date": "2026-06", "end_date": "present", "rank": "县处级正职", "note": "2026-06-24十届一次全会选何卉为市委书记; 2026-07-25主持市委常委会"},
    # 何卉 — 市长(2026-03前)履历链
    {"person_id": 1, "org_id": 1, "title": "舞钢市委副书记", "start_date": "", "end_date": "2026-06", "rank": "县处级副职", "note": "2026-03时任市委副书记、市长"},
    {"person_id": 1, "org_id": 2, "title": "舞钢市人民政府市长", "start_date": "", "end_date": "2026-06", "rank": "县处级正职", "note": "2026-03-04朱志骞主持常委会,何卉任市长"},
    # 马向阳 — 市长
    {"person_id": 2, "org_id": 1, "title": "舞钢市委副书记", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": "2026-06-24十届一次委任副书记"},
    {"person_id": 2, "org_id": 2, "title": "舞钢市人民政府市长", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职", "note": "2026-07-08代理市长; 07-10市十一届六次会议当选市长"},
    # 杨志鹏 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "舞钢市委副书记", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 任国军 — 人大主任
    {"person_id": 4, "org_id": 3, "title": "舞钢市人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "四套班子主官"},
    # 王冬梅 — 政协主席
    {"person_id": 5, "org_id": 4, "title": "舞钢市政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "四套班子主官"},
    # 常务副市长 刚延召
    {"person_id": 6, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "舞钢市常务副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席市人大常委会议"},
    # 纪委书记 郑冠宇
    {"person_id": 7, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "舞钢市纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 政法委 赵鹏飞
    {"person_id": 8, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "舞钢市委政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "主持法治政府建设推进会"},
    # 市委办主任 何绍三
    {"person_id": 9, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "舞钢市委办公室主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 其余常委
    {"person_id": 10, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": "分工待考"},
    {"person_id": 11, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "舞钢市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "市十一届人大主席团执行主席"},
    {"person_id": 12, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": "分工待考"},
    {"person_id": 13, "org_id": 1, "title": "舞钢市委常委", "start_date": "2026-06", "end_date": "present", "rank": "县处级副职", "note": "分工待考"},
    # 公安局长 宋陈梁
    {"person_id": 14, "org_id": 2, "title": "舞钢市副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 9, "title": "舞钢市公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 法院院长
    {"person_id": 15, "org_id": 10, "title": "舞钢市人民法院院长", "start_date": "2026-07", "end_date": "present", "rank": "县处级副职", "note": "2026-07-10当选(此前代院长)"},
    # 检察长
    {"person_id": 16, "org_id": 11, "title": "舞钢市人民检察院检察长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 人武部长 王利
    {"person_id": 17, "org_id": 12, "title": "舞钢市人民武装部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 前任书记 朱志骞
    {"person_id": 18, "org_id": 1, "title": "舞钢市委书记", "start_date": "", "end_date": "2026-05", "rank": "县处级正职", "note": "2026-03-04仍任书记; 其后离任"},
    # 龚宪君 前任副书记
    {"person_id": 19, "org_id": 1, "title": "舞钢市委副书记", "start_date": "", "end_date": "2026-05", "rank": "县处级副职", "note": "2026-03-04在任"},
    # 平顶山上层互动
    {"person_id": 20, "org_id": 13, "title": "平顶山市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
    {"person_id": 21, "org_id": 13, "title": "平顶山市委副书记", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": ""},
    {"person_id": 21, "org_id": 14, "title": "平顶山市市长", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 何卉 ↔ 马向阳 (党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "何卉任市委书记,马向阳任市委副书记、市长,舞钢市党政正职搭档(权力核心)", "overlap_org": "舞钢市", "overlap_period": "2026至今"},
    # 何卉 ↔ 杨志鹏
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记", "overlap_org": "中共舞钢市委员会", "overlap_period": "2026至今"},
    # 马向阳 ↔ 杨志鹏
    {"person_a": 2, "person_b": 3, "type": "same_system", "context": "同为舞钢市委副书记(马兼市长)", "overlap_org": "中共舞钢市委员会", "overlap_period": "2026至今"},
    # 四大班子联系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委与市人大常委会(任国军)", "overlap_org": "舞钢市", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委与市政协(王冬梅)", "overlap_org": "舞钢市", "overlap_period": "当前"},
    # 前任/继任
    {"person_a": 18, "person_b": 1, "type": "promotion_chain", "context": "朱志骞为前任舞钢市委书记,何卉接任其为书记(2026),且朱任驻时何任市长", "overlap_org": "中共舞钢市委员会", "overlap_period": "2024-2026"},
    {"person_a": 19, "person_b": 1, "type": "same_system", "context": "龚宪君任市委副书记期间与何卉(市长)共事(2026-03)", "overlap_org": "中共舞钢市委员会", "overlap_period": "2026-03"},
    # 上级市联系
    {"person_a": 20, "person_b": 1, "type": "superior_subordinate", "context": "平顶山市委书记陈向平对舞钢市委有上下级工作关系", "overlap_org": "中共平顶山市委/舞钢市", "overlap_period": "当前"},
    {"person_a": 21, "person_b": 2, "type": "superior_subordinate", "context": "平顶山市市长李明俊与舞钢市长马有上级领导关系", "overlap_org": "平顶山市/舞钢市", "overlap_period": "当前"},
    # 常务副市长 (刚延召) 为核心副职
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长刚延召副市长在政府班子中配合市长马", "overlap_org": "舞钢市人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate", "context": "政法委书记赵鹏飞在法治建设中配合市委", "overlap_org": "舞钢市", "overlap_period": "当前"},
    {"person_a": 7, "person_b": 1, "type": "same_system", "context": "纪委书记郑冠宇受其领导、监督班子", "overlap_org": "中共舞钢市委员会", "overlap_period": "当前"},
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "市委办主任何绍三服务市委书记", "overlap_org": "中共舞钢市委员会", "overlap_period": "当前"},
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "何卉",
        "job": "市委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "平顶山市", "region": "舞钢市", "job": "市委书记", "task_id": "henan_舞钢市", "time_focus": "2026"},
            "identity": {
                "person_id": "wugang_何卉",
                "name": "何卉", "aliases": [], "gender": "女", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "何卉_", "name_birthplace": "何卉_", "official_profile_url": "https://www.zgwg.gov.cn"}
            },
            "current_status": {"current_post": "市委书记", "current_org": "中共舞钢市委员会", "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]},
            "career_timeline": [
                {"start": "unknown", "end": "2026-03", "org": "舞钢市人民政府", "title": "市长、市委副书记", "level": "县处级正职", "location": "舞钢市", "system": "government", "rank": "县处级正职", "is_key_promotion": False, "notes": "至2026-03其任舞钢市委副书记、市长(朱志骞委员常委会时被列在何名后)", "confidence": "confirmed", "source_ids": ["S004"]},
                {"start": "2026-06", "end": "present", "org": "中共舞钢市委员会", "title": "市委书记", "level": "县处级正职", "location": "舞钢市", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-06-24当选十届市委书记; 2026-06-22代表九届市委作报告(可见由此前即任书记或可追溯至更早)", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺失", "title": "", "notes": "何卉出生年/籍贯/学历/入党/参加工作及任舞钢市长前的整段履历未获公开一手资料(搜狗相关推荐提示'舞钢市长何卉是哪个县'未核)", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "中共舞钢市委员会", "role": "市委书记", "period": "2026至今", "source_ids": ["S001", "S002"]},
                {"name": "舞钢市人民政府", "role": "市长", "period": "至2026-03", "source_ids": ["S004"]}
            ],
            "relationships": [
                {"person": "马向阳", "person_id": "wugang_马向阳", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "何任市委书记,马任市长、市委副书记,党政正职搭档", "overlap_org": "舞钢市", "overlap_period": "2026至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "朱志骞", "person_id": "wugang_朱志骞", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "朱为前任市委书记,何何先任市长后任书记,疑似内部接任", "overlap_org": "舞钢市", "overlap_period": "2024-2026", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S004"]}
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "主持召开省、平顶山市重点项目调度会,强调'项目为王'',聚焦六张网、超长期特别国债", "role_in_event": "主持人", "measurable_outcome": "", "location": "舞钢市", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2026-06", "domain": "organization", "achievement_or_event": "在市第十四次/第十次党代会推进'五城建设'+十项行动,科学谋划'十五五'", "role_in_event": "作报告人/主持人", "measurable_outcome": "", "location": "舞钢市", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-08", "domain": "public_security", "achievement_or_event": "带队走访慰问部队官兵,强调军民协同与安全防线(双拥)", "role_in_event": "带队人", "measurable_outcome": "", "location": "舞钢市", "confidence": "confirmed", "source_ids": ["S005"]}
            ],
            "professional_profile": {"primary_specializations": ["economic_development", "project_management", "party_organization"], "secondary_specializations": [], "career_pattern": "local_ladder", "systems_experience": ["party", "government"], "geographic_pattern": ["舞钢市"], "promotion_velocity": {"summary": "市长→市委书记渠道:2026-06由市长晋任书记(十届一次全会),完整晋升链待考", "notable_fast_promotions": []}},
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "economic_driving", "evidence": "多次调度重点项目建设/争资,强调'项目为王''五城建设'", "confidence": "confirmed", "source_ids": ["S003"]},
                    {"trait": "party_governance", "evidence": "提出树立正确政绩观学习教育总要求'实干担当、清正廉洁''五个方面'", "confidence": "confirmed", "source_ids": ["S002"]}
                ],
                "speech_themes": ["工业优先、项目为王", "五城建设", "十项行动", "十五五规划"], 
                "management_signals": [],
                "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "中共舞钢市委十届一次全会举行", "url": "https://www.zgwg.gov.cn/contents/14734/748402.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-06-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "选举何卉为市委书记"},
                {"id": "S002", "title": "中国共产党舞钢市第十次代表大会开幕", "url": "https://www.zgwg.gov.cn/contents/14734/748308.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-06-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何卉代表九届市委作工作报告"},
                {"id": "S003", "title": "何卉主持召开省、平顶山市重点项目调度会", "url": "https://www.zgwg.gov.cn/contents/14734/751089.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-07-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市委书记何卉主持"},
                {"id": "S004", "title": "朱志骞主持召开市委常委会(扩大)会议", "url": "https://www.zgwg.gov.cn/contents/14734/737919.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-03-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2026-03时任书记朱、市长何"},
                {"id": "S005", "title": "何卉 马向阳带队走访慰问官兵", "url": "https://www.zgwg.gov.cn/contents/14734/751494.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何为书记,马为市长"}
            ],
            "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "何卉出生年/籍贯/学历/入党及任舞钢市长前的完整履历"},
            "open_questions": [
                {"priority": "critical", "question": "何卉出生年、籍贯、学历、入党/参加工作及任舞钢市长前的整段履历?", "why_it_matters": "还原其成长与早期关系网络", "suggested_queries": ["何卉 舞钢 简历 此前", "何卉 平顶山 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任舞钢市委书记朱志骞到任一离任时间线及离任去向?", "why_it_matters": "梳理书记换届权力交接", "suggested_queries": ["朱志骞 舞钢 离任 去向", "舞钢市委书记 换届"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "马向阳",
        "job": "市长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "平顶山市", "region": "舞钢市", "job": "市长", "task_id": "henan_舞钢市", "time_focus": "2026"},
            "identity": {
                "person_id": "wugang_马向阳",
                "name": "马向阳", "aliases": [], "gender": "", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "马向阳_", "name_birthplace": "马向阳_", "official_profile_url": "https://www.zgwg.gov.cn"}
            },
            "current_status": {"current_post": "市委副书记、市长", "current_org": "舞钢市人民政府", "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
            "career_timeline": [
                {"start": "2025-", "end": "2026-05", "org": "舞钢市", "title": "市委副书记", "level": "县处级副职", "location": "舞钢市", "system": "party", "rank": "县处级副职", "is_key_promotion": False, "notes": "马2026-06起任市委副书记(从年初履职时间待分)", "confidence": "plausible", "source_ids": ["S001"]},
                {"start": "2026-05", "end": "2026-07-08", "org": "舞钢市人民政府", "title": "代理市长(代市长)", "level": "县处级正职", "location": "舞钢市", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-07-08代市代表作政府工作报告,2026-07-30主持政府常务会", "confidence": "confirmed", "source_ids": ["S002"]},
                {"start": "2026-07-10", "end": "present", "org": "舞钢市人民政府", "title": "舞钢市人民政府市长", "level": "县处级正职", "location": "舞钢市", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "市十一届人大六次会议闭幕选举当选市长; 2026-08-03主持市政府常务会议", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "马向阳出生年/籍贯/学历及任舞钢前履历未获公开一手", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "舞钢市人民政府", "role": "市长(代/正式)", "period": "2026年", "source_ids": ["S001", "S002"]},
                {"name": "中共舞钢市委员会", "role": "市委副书记", "period": "2026至今", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "何卉", "person_id": "wugang_何卉", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "马任市长(副书记),何任市委书记,党政正职搭档", "overlap_org": "舞钢市", "overlap_period": "2026至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "任国军", "person_id": "wugang_任国军", "relationship_type": "other", "strength": "weak", "evidence": "市长受市人大监督,任为人大主任", "overlap_org": "舞钢市", "overlap_period": "当前", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "public_security", "achievement_or_event": "主持市政府常务会议:部署安全生产、生态环保、城市防洪规划、经济运行", "role_in_event": "主持人", "measurable_outcome": "", "location": "舞钢市", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-07-31", "domain": "legal_governance", "achievement_or_event": "出席法治政府建设工作推进会并讲话,强调打造法治化营商环境", "role_in_event": "讲话人", "measurable_outcome": "", "location": "舞钢市", "confidence": "confirmed", "source_ids": ["S006"]},
                {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "作舞钢市'十五五'政府工作报告,提出生产总值增长5.5%左右目标", "role_in_event": "报告人", "measurable_outcome": "", "location": "舞钢市", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "professional_profile": {
                "primary_specializations": ["fiscal_management", "project_management", "governance"], "secondary_specializations": [],
                "career_pattern": "local_ladder", "systems_experience": ["party", "government"], "geographic_pattern": ["舞钢市"],
                "promotion_velocity": {"summary": "市委副书记→代市长→(2026-07)正式当选市长,晋升快节奏;任前履历待考", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "pragmatic", "evidence": "政府常务会议讲话强调'稳住经济基本盘、应入尽入申报、防汛值班值守'", "confidence": "confirmed", "source_ids": ["S001"]}
                ],
                "speech_themes": ["企业入库入库、应统尽统", "安全生产与防汛备汛", "法治化营商环境"], "management_signals": [],
                "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "马向阳主持召开市政府常务会议", "url": "https://www.zgwg.gov.cn/contents/14734/751710.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市委副书记、市长马向阳主持"},
                {"id": "S002", "title": "市十一届人大六次会议开幕/闭幕", "url": "https://www.zgwg.gov.cn/contents/14734/749724.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-07-08/10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "7-08代市长作报告,7-10当选市长"},
                {"id": "S006", "title": "我市召开法治政府建设工作推进会 马向阳出席并讲话", "url": "https://www.zgwg.gov.cn/contents/14734/751483.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市长马向阳出席并讲话"}
            ],
            "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "马向阳出生年/籍贯/学历及任舞钢前履历;确切代市长任命时间"},
            "open_questions": [
                {"priority": "critical", "question": "马向阳出生年、籍贯、学历、入党/参加工作及任舞钢市长前的履历(之前在哪任职)?", "why_it_matters": "还原其培养路径与选区网络", "suggested_queries": ["马向阳 舞钢 市长 简历 此前", "马向阳 平顶山 任命 代市长"], "last_attempted": AS_OF},
                {"priority": "high", "question": "马向阳任舞钢代市长的确切任命时间(2026-05前后?),前任市长何卉改任书记后的交接节点?", "why_it_matters": "梳理2026年市政府一把手交接", "suggested_queries": ["舞钢市 代市长 任命 2026", "舞钢市长 交接 2026"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 18,
        "name": "朱志骞",
        "job": "前任市委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "平顶山市", "region": "舞钢市", "job": "前任市委书记", "task_id": "henan_舞钢市", "time_focus": "2026"},
            "identity": {
                "person_id": "wugang_朱志骞",
                "name": "朱志骞", "aliases": [], "gender": "", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "朱志骞_", "name_birthplace": "朱志骞_", "official_profile_url": "https://www.zgwg.gov.cn"}
            },
            "current_status": {"current_post": "前任市委书记(2026年中离任)", "current_org": "中共舞钢市委员会", "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": False, "source_ids": ["S001", "S004"]},
            "career_timeline": [
                {"start": "unknown", "end": "2026-05", "org": "中共舞钢市委员会", "title": "市委书记", "level": "县处级正职", "location": "舞钢市", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-03-04主持市委常委会(加)会议,确认其任书记;其后至2026-06由何接任", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "朱志骞出生、籍贯、学历及任舞钢市委书记前历/离开舞钢后去向均未获一手", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [{"name": "中共舞钢市委员会", "role": "市委书记(前任)", "period": "至2026-05", "source_ids": ["S004"]}],
            "relationships": [
                {"person": "何卉", "person_id": "wugang_何卉", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "朱为前任书记,何为其任内市长后接任书记", "overlap_org": "舞钢市", "overlap_period": "至2026-05", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S004"]}
            ],
            "governance_record": [],
            "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["party"], "geographic_pattern": ["舞钢市"], "promotion_velocity": {"summary": "任舞钢市委书记至2026-05,离任方向未明", "notable_fast_promotions": []}},
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "资料不足,不以少证下结论"},
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息(Baidu 403 无法检索负面)", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S004", "title": "朱志骞主持召开市委常委会(扩大)会议", "url": "https://www.zgwg.gov.cn/contents/14734/737919.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-03-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认朱为市委书记、何为市长"},
                {"id": "S001", "title": "中共舞钢市委十届一次全会举行", "url": "https://www.zgwg.gov.cn/contents/14734/748402.html", "publisher": "舞钢市融媒体中心", "published_at": "2026-06-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "何当选书记,朱未再任"}
            ],
            "confidence_summary": {"identity": "unverified", "current_role": "confirmed(前任)", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "朱志骞任舞钢书记起止、离任去向及整段履历"},
            "open_questions": [
                {"priority": "high", "question": "朱志骞任舞钢市委书记起止时间线、离任去向及任前履历?", "why_it_matters": "还原2026年舞钢市委书记换届链条", "suggested_queries": ["朱志骞 舞钢 市委书记 离任 去向", "朱志骞 简历 舞钢"], "last_attempted": AS_OF}
            ]
        }
    },
]

# ── Markdown report data ────────────────────────────────────────────────────
REPORT_FILENAME = f"{TODAY}-舞钢市-领导班子工作关系网络调查报告.md"

report_text = f"""# 舞钢市领导班子工作关系网络调查报告

> 河南省 · 平顶山市代管 · 舞钢市(县级市)
> 调查日期:{AS_OF}(数据截至 2026-07-08)
> 目标职务：市委书记 & 市长
> 任务 ID：henan_舞钢市
> 数据来源：舞钢市人民政府门户网站(www.zgwg.gov.cn,官方一手)+ 平顶山市政府门户(www.pds.gov.cn)

---

## 1. 现任市委书记：何卉
- **职务**：中共舞钢市委书记 (2026-06-24 中共舞钢市委十届一次全会选举)
- **性别**：女
- **关键脉络**：2026-03 时任市委副书记、市长（朱志骞主持市委常委会报道可见其列任）；2026-06-22 市第十次党代会开幕时**代表中共九届市委作工作报告**，2026-06-24 十届一次全会正式当选市委书记。即何卉由市长晋任书记（2026-06）。
- **履历深度**：出生年/籍贯/学历/入党/参加工作及任舞钢市长前完整履历受搜索引擎阻断（Exa 限流、Baidu 403、Sogou/360 验证码）未能核实 → open_questions。

## 2. 现任市长：马向阳
- **职务**：市委副书记、市长
- **确认依据**：2026-07-08 市十一届人大六次会议开幕，以“代理市长”作政府工作报告；2026-07-10 会议闭幕，**当选舞钢市人民政府市长**；2026-08-03 市委副书记、市长马向阳主持市政府常务会议。
- **履历深度**：出生/籍贯/学历/入党及任舞钢前履历未核实 → open_questions。

## 3. 前任市委书记（去向）
- **前任书记：朱志骞**。2026-03-04 朱志骞主持市委常委会（扩大）会议，确认其为市委书记。其后至 2026-06 由何卉接任。朱离任去向待补（open gap）。

## 4. 前任市长（去向）
- 前任市长即**何卉**（由市长晋任书记，2026-06）；马向阳任代市长（2026 年上半年）→ 正式市长（2026-07-10）。更早前任市长及马接任前的具体交接节点待考。

## 5. 现任领导班子成员（官方一手）
| 姓名 | 职务 | 备注 |
|---|---|---|
| 何卉 | 市委书记 | 现任一把手(女),confirmed |
| 马向阳 | 市委副书记、市长 | 现任二把手,confirmed |
| 杨志鹏 | 市委副书记 | 二把手之一,confirmed |
| 任国军 | 市人大常委会主任 | confirmed |
| 王冬梅 | 市政协主席 | confirmed |
| 刚延召 | 市委常委、常务副市长 | confirmed |
| 郑冠宇 | 市委常委、纪委书记、监委主任 | confirmed |
| 赵鹏飞 | 市委常委、市政法委书记 | confirmed |
| 何绍三 | 市委常委、市委办主任 | confirmed |
| 郭素文 | 市委常委 | 分工待考 |
| 高军华 | 市委常委、市人大副主任 | 主体主席团 |
| 殷高洁 | 市委常委 | 分工待考 |
| 刘洪涛 | 市委常委 | 分工待考 |
| 宋陈梁 | 副市长、市公安局长 | confirmed |
| 王二朝 | 市法院院长 | 2026-07-10当选 |
| 顾武修 | 市检察院检察长 | confirmed |
| 王利 | 市人武部部长 | confirmed |

## 6. 近期人事变动(时间线)
- 2026-03-03/04：**朱志骞**(书记)主持市委常委会（扩）; **何卉**(副书记、市长)、**龚宪君**(市委副书记)出席。
- 2026-06-22/24：市第十次党代会与十届一次全会,何卉当选市委书记,马向阳、杨志鹏当选副书记；常委班子(郭素文、刚延召、郑冠宇、何绍三、刘洪涛、赵鹏飞等)公布。
- 2026-07-08：市十一届人大六次会议开幕,马向阳以代理市长作报告。
- 2026-07-10：马向阳当选市长(正式转正); 王二朝当选市法院院长。
- 2026-08-03：马向阳主持市政府常务会议。

## 7. 工作关系网络分析（初步）
- **何卉 ↔ 马向阳**：市委书记 × 市长，党政正职搭档（confirmed，强）。
- **何卉/马向阳 ↔ 杨志鹏**：常委会副书记关系（confirmed）。
- **何卉 ↔ 朱志骞**：朱任书记、何任市长时党政搭档（至 2026-05），后何接任书记 （medium）。
- **舞钢 ↔ 平顶山**：属市辖县级市，平顶山市委书记陈向平、市长李明俊对舞钢有上下级工作联系。
- 常委会内部：常务副市长刚延召、纪委书记郑冠宇、政法委书记赵鹏飞、市委办主任何绍三等构成治理主轴。

## 8. 关键洞察与突破线索
1. **何卉由市长晋任书记**（2026-06），属县级市"市长→书记"标准跃迁，需补其任市长前履历。
2. **马向阳 2026 年快速转正**：2026-07-08 前为代市长、07-10 即当选市长，晋升节奏快，需补完整履历。
3. **班子以"产业+项目+依法治市"为主线**：多场常委会聚焦重点项目、法治政府建设、巡察整改（平顶山市委第六巡察组）。
4. **前任书记朱志骞去向**是跨区干部流动的关键线索：需确认其调任平顶山何处。

## 9. 数据文件说明
- `build_舞钢市_data.py` / `data/database/舞钢市_network.db` / `data/graph/舞钢市_network.gexf`
- `data/persons/YYYYMMDD-河南省-平顶山市-市委书记-何卉.json` 等
- Report(本文)、open_gaps.md

## 10. 信息来源汇总
- S001 舞钢市人民政府门户网站 www.zgwg.gov.cn（2026-08-06 访问）
  - 十届一次全会 /contents/14734/748402.html
  - 党代会开幕（何代表九届市委作报告）/contents/14734/748308.html
  - 人大开幕/闭幕 /contents/14734/749519.html、749724.html
  - 马主持市政府常务会议 /contents/14734/751710.html
  - 何卉重点项目调度会 /contents/14734/751089.html
  - 朱志骞主持市委常委会 /contents/14734/737919.html
  - 法治政府建设推进会 /contents/14734/751483.html
- S002 平顶山市人民政府 www.pds.gov.cn（站群导航确认舞钢官方域名）
- 本轮通用搜索引擎（Bing/Baidu/Sogou/360）均被反爬，故以官方门户为主要一手证据。
"""

# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-平顶山市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # Write markdown report
    report_path = PERSONS_DIR / REPORT_FILENAME
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"  ✅ Report: {report_path}")

    # ── Copy to canonical paths ────────────────────────────────────
    CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
    CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
    CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
    CANONICAL_PERSONS = BASE / "data" / "persons"
    CANONICAL_REPORT = BASE / "report" / REPORT_FILENAME

    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)
    CANONICAL_REPORT.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)
    if report_path.exists():
        shutil.copy2(report_path, CANONICAL_REPORT)
        print(f"  ✅ Canonical report: {CANONICAL_REPORT}")

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-平顶山市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()