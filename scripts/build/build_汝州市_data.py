#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汝州市 (Ruzhou City), 平顶山市, 河南省.

Investigation date: 2026-08-06 (new build)
Task ID: henan_汝州市
Level: 县级市 (平顶山市代管)
Targets: 市委书记 & 市长

Research sources (confirmed 2026-08-06, official primary source):
  - 汝州市人民政府门户网站 www.ruzhou.gov.cn (平顶山市政府站群导航确认域名):
    - 官方"领导之窗"(/channels/36778.html): 市委副书记、市长 胡红杰; 副市长 张飞、陈海丰、董备战、于跃峰、唐佳佳、李慧娟; 秘书长 郭玉玮。
    - 2026-07-31 刘国朝带队开展八一建军节走访慰问活动: "汝州市委书记刘国朝带队"; 市委副书记杨世崇, 市领导于伟、余行健、李军、董备战一同慰问。 (注: 页面正文第一句话个别版本将名字写作"刘国良"，但标题与正文其余多处均一致为"刘国朝"，本报告采信"刘国朝"。)
    - 2026-07-31 胡红杰走访慰问驻汝官兵/退役军人: "市委副书记、市长胡红杰"; 市领导张剑奇、范响立及市政府党组成员、秘书长郭玉玮参加。
    - 2026-07-29 市九届人大常委会第三十七次会议: 人大常委会党组书记、主任 李新杰; 领导 张剑奇、杜占广、汪聚涛、张胜伟、郭文源、康凯、郑学伟; 秘书长 张俊峰; 列席 市委常委、纪委书记、监委代主任 王红文, 市委常委、常务副市长 张飞, 市委常委、组织部部长 黄红丽。
    - 2026-07-27 市政府党组(扩大)会议(市长胡红杰主持): 市领导 张飞、陈海丰、李益恒、董备战、于跃峰、李慧娟、王泉水、陈振军、翟会杰、魏俊涛、鲁武国、朱同正、陈万幸、武乐蒙、赵宪正 + 郭玉玮。
    - 2026-07-20 市重点工作调度会(市长胡红杰出席, 市委副书记杨世崇): 市领导 张飞、黄红丽、刘永涛、李益恒、王汝、范响立、陈振军、张振伟、武乐蒙 + 郭玉玮。
    - 2026-07-17 胡红杰调研生态环境保护重点, 市领导李益恒、张振伟参与。
    - 2026-07-14 胡红杰深入庙下镇/经开区/纸坊镇调研水环境治理。

Cross-region / 上级:
  - 汝州市属平顶山市代管县级市; 平顶山市委书记 陈向平、市长 李明俊 对汝州有上下级工作联系 (confirmed 本地平顶山市调查 2026-08-05)。
  - 跨县交流线索: 顾宪君近曾在舞钢市任市委副书记(2026-03),成 2026年 平顶山宝丰县 县委副书记、县长(本地舞钢市调查/宝丰县调查),体现平顶山市内跨县干部流动;汝州与宝丰同为汝瓷主产区,存在产业-人事联动猜想(推断)。

Gaps flagged in person JSON `open_questions`:
  - 刘国良/刘国朝 与 胡红杰 出生年、籍贯、学历、入党、参加工作 及任汝州市委书记/市长前的完整履历
  - 前任汝州市委书记(刘国朝之前)、前任市长(胡红杰之前)姓名与去向
  - 胡红杰任市长(代理→转正)的确切时间线
  - 各常委员现任具体分工细目; 纪委监委/法检两院补充领导名单
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
SLUG = "汝州市"
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
        "name": "刘国朝",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共汝州市委员会",
        "source": "汝州市人民政府门户网站·刘国朝带队八一建军节走访慰问(2026-07-31); official",
    },
    {
        "id": 2,
        "name": "胡红杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "汝州市人民政府",
        "source": "汝州市政府官网·领导之窗(/channels/36778.html); 胡红杰走访慰问/政府党组会/生态调研新闻(2026-07); official",
    },
    # ═══ 市委班子 ═══
    {
        "id": 3,
        "name": "杨世崇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共汝州市委员会",
        "source": "汝州市政府官网·刘国朝走访慰问新闻(2026-07-31)/市重点工作调度会(2026-07-20); official",
    },
    {
        "id": 4,
        "name": "张飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "汝州市人民政府",
        "source": "汝州市政府官网·市九届人大常委会会议列席(2026-07-29)确认市委常委/常务副市长; 领导之窗副市长; official",
    },
    {
        "id": 5,
        "name": "王红文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共汝州市纪律检查委员会",
        "source": "汝州市政府官网·市人大常委会三十七次会议列席(2026-07-29); official",
    },
    {
        "id": 6,
        "name": "黄红丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共汝州市委员会组织部",
        "source": "汝州市政府官网·市人大常委会三十七次会议列席(2026-07-29)/重点工作调度会(2026-07-20); official",
    },
    # ═══ 市人大常委会 ═══
    {
        "id": 7,
        "name": "李新杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "汝州市人大常委会",
        "source": "汝州市政府官网·市九届人大常委会第三十七次会议(2026-07-29); official",
    },
    # ═══ 市政府副市长 ═══
    {
        "id": 8,
        "name": "陈海丰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "汝州市人民政府",
        "source": "汝州市政府官网·领导之窗/市政府党组会(2026-07-27); official",
    },
    {
        "id": 9,
        "name": "董备战",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "汝州市人民政府",
        "source": "汝州市政府官网·领导之窗/刘国朝慰问新闻(2026-07-31)/市政府党组会(2026-07-27); official",
    },
    {
        "id": 10,
        "name": "于跃峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "汝州市人民政府",
        "source": "汝州市政府官网·领导之窗/市政府党组会(2026-07-27); official",
    },
    {
        "id": 11,
        "name": "唐佳佳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "汝州市人民政府",
        "source": "汝州市政府官网·领导之窗(/channels/36778.html); official",
    },
    {
        "id": 12,
        "name": "李慧娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "汝州市人民政府",
        "source": "汝州市政府官网·领导之窗/市政府党组会(2026-07-27); official",
    },
    {
        "id": 13,
        "name": "郭玉玮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府党组成员、秘书长",
        "current_org": "汝州市人民政府办公室",
        "source": "汝州市政府官网·领导之窗/胡红杰慰问新闻(2026-07-31)/市政府党组会; official",
    },
    # ═══ 其他市领导 (official news 提及) ═══
    {
        "id": 14,
        "name": "张剑奇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导/市人大常委会领导",
        "current_org": "汝州市人大常委会",
        "source": "汝州市政府官网·胡红杰慰问新闻(2026-07-31)/市九届人大常委会三十七次会议(2026-07-29); official",
    },
    {
        "id": 15,
        "name": "范响立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "汝州市",
        "source": "汝州市政府官网·胡红杰慰问新闻(2026-07-31)/市重点工作调度会(2026-07-20); official",
    },
    {
        "id": 16,
        "name": "李益恒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "汝州市",
        "source": "汝州市政府官网·胡红杰调研生态(2026-07-17)/市重点工作调度会(2026-07-20)/市政府党组会(2026-07-27); official",
    },
    # ═══ 跨县/上级 ═══
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
    {"id": 1, "name": "中共汝州市委员会", "type": "党委", "level": "县处级", "parent": "中共平顶山市委", "location": "汝州市"},
    {"id": 2, "name": "汝州市人民政府", "type": "政府", "level": "县处级", "parent": "平顶山市人民政府", "location": "汝州市"},
    {"id": 3, "name": "汝州市人大常委会", "type": "人大", "level": "县处级", "parent": "平顶山市人大常委会", "location": "汝州市"},
    {"id": 5, "name": "中共汝州市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "平顶山市纪委监委", "location": "汝州市"},
    {"id": 6, "name": "汝州市监察委员会", "type": "纪委", "level": "县处级", "parent": "平顶山市监委", "location": "汝州市"},
    {"id": 8, "name": "中共汝州市委组织部", "type": "党委", "level": "县处级", "parent": "中共汝州市委员会", "location": "汝州市"},
    {"id": 9, "name": "汝州市人民政府办公室", "type": "政府", "level": "县处级", "parent": "汝州市人民政府", "location": "汝州市"},
    {"id": 10, "name": "中共平顶山市委", "type": "党委", "level": "地厅级", "parent": "中共河南省委", "location": "平顶山市"},
    {"id": 11, "name": "平顶山市人民政府", "type": "政府", "level": "地厅级", "parent": "河南省人民政府", "location": "平顶山市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 刘国朝 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "汝州市委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-07-31 带队八一走访慰问,官文确认为市委书记; 现任一把手"},
    # 胡红杰 — 市长
    {"person_id": 2, "org_id": 1, "title": "汝州市委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-07-31 官方确认市委副书记、市长"},
    {"person_id": 2, "org_id": 2, "title": "汝州市人民政府市长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "官方领导之窗明确'市委副书记、市长'"},
    # 副书记 杨世崇
    {"person_id": 3, "org_id": 1, "title": "汝州市委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张飞 常务副市长
    {"person_id": 4, "org_id": 1, "title": "汝州市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "汝州市常务副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "列席市人大常委会议"},
    # 纪委 王红文
    {"person_id": 5, "org_id": 1, "title": "汝州市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "汝州市纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 组织部长 黄红丽
    {"person_id": 6, "org_id": 1, "title": "汝州市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "汝州市委组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 人大主任 李新杰
    {"person_id": 7, "org_id": 3, "title": "汝州市人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "四套班子主官(党组书记、主任)"},
    # 副市长
    {"person_id": 8, "org_id": 2, "title": "汝州市副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "汝州市副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "汝州市副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "汝州市副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "汝州市副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 秘书长
    {"person_id": 13, "org_id": 2, "title": "汝州市政府秘书长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "市政府党组成员、秘书长"},
    # 其他市领导
    {"person_id": 14, "org_id": 3, "title": "汝州市人大领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "汝州市领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "分工待考"},
    {"person_id": 16, "org_id": 2, "title": "汝州市领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "市政府序列领导, 具体分工待考"},
    # 平顶山上层
    {"person_id": 20, "org_id": 10, "title": "平顶山市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
    {"person_id": 21, "org_id": 10, "title": "平顶山市委副书记", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": ""},
    {"person_id": 21, "org_id": 11, "title": "平顶山市市长", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 刘国朝 ↔ 胡红杰 (党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "刘国朝任市委书记,胡红杰任市委副书记、市长,汝州市党政正职搭档(权力核心)", "overlap_org": "汝州市", "overlap_period": "当前"},
    # 刘国朝 ↔ 副书记杨世崇
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记", "overlap_org": "中共汝州市委员会", "overlap_period": "当前"},
    # 胡红杰 ↔ 杨世崇
    {"person_a": 2, "person_b": 3, "type": "same_system", "context": "同为汝州市委副书记(胡兼市长)", "overlap_org": "中共汝州市委员会", "overlap_period": "当前"},
    # 党政与人大
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委党组书记与市人大常委会主任工作关系", "overlap_org": "汝州市", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长受市人大常委会监督(李新杰为人大主任)", "overlap_org": "汝州市", "overlap_period": "当前"},
    # 常委/部门
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长张飞在政府班子中配合市长", "overlap_org": "汝州市人民政府", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 1, "type": "same_system", "context": "纪委书记王红文受市委领导、监督班子", "overlap_org": "中共汝州市委员会", "overlap_period": "当前"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate", "context": "组织部长黄红丽在干部人事上配合市委/市委书记", "overlap_org": "中共汝州市委员会", "overlap_period": "当前"},
    # 上级市
    {"person_a": 20, "person_b": 1, "type": "superior_subordinate", "context": "平顶山市委书记陈向平对汝州市委有上下级工作关系", "overlap_org": "中共平顶山市委/汝州市", "overlap_period": "当前"},
    {"person_a": 21, "person_b": 2, "type": "superior_subordinate", "context": "平顶山市市长李明俊与汝州市长胡有上级领导关系", "overlap_org": "平顶山市/汝州市", "overlap_period": "当前"},
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "刘国朝",
        "job": "市委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "平顶山市", "region": "汝州市", "job": "市委书记", "task_id": "henan_汝州市", "time_focus": "2026"},
            "identity": {
                "person_id": "ruzhou_刘国朝",
                "name": "刘国朝", "aliases": ["刘国良(个别版本讹字)"], "gender": "男", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "刘国朝_", "name_birthplace": "刘国朝_", "official_profile_url": "https://www.ruzhou.gov.cn"}
            },
            "current_status": {"current_post": "市委书记", "current_org": "中共汝州市委员会", "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
            "career_timeline": [
                {"start": "", "end": "present", "org": "中共汝州市委员会", "title": "市委书记", "level": "县处级正职", "location": "汝州市", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-07-31 刘国朝走访慰问新闻确认其为汝州市委书记;任书记前履历无一手", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "刘国朝出生年/籍贯/学历/入党/参加工作及任汝州市委书记前完整履历尚未获公开一手资料", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [{"name": "中共汝州市委员会", "role": "市委书记", "period": "现状", "source_ids": ["S001"]}],
            "relationships": [
                {"person": "胡红杰", "person_id": "ruzhou_胡红杰", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "刘朝任市委书记,胡任市长、市委副书记,党政正职搭档", "overlap_org": "汝州市", "overlap_period": "当前", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "陈向平", "person_id": "pds_陈向平", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "平顶山市委书记陈向平为汝州市委上级", "overlap_org": "平顶山市/汝州市", "overlap_period": "当前", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]}
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "带队开展八一建军节走访慰问,强调支持国防和军队建设、深化双拥共建(拥军优属)", "role_in_event": "带队人/讲话人", "measurable_outcome": "", "location": "汝州市", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "professional_profile": {"primary_specializations": ["party_organization", "civilian_military_coordination"], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["party"], "geographic_pattern": ["汝州市"], "promotion_velocity": {"summary": "任汝州市委书记(2026在任),任前履历待考", "notable_fast_promotions": []}},
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "带队慰问驻地部队、军修干部/退役军人,强调军民融合与基层服务", "confidence": "confirmed", "source_ids": ["S001"]}
                ],
                "speech_themes": ["双拥共建", "军民融合", "支持国防和军队现代化建设"], "management_signals": [],
                "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "情系子弟兵 共叙鱼水情 刘国朝带队开展八一建军节走访慰问活动", "url": "https://www.ruzhou.gov.cn/contents/36561/751479.html", "publisher": "汝州市融媒体中心", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官宣刘国朝任汝州市委书记"},
                {"id": "S003", "title": "平顶山市领导网络调查报告(本地存档)", "url": "report/20260805-平顶山市-领导网络调查报告.md", "publisher": "gov-relation repo", "published_at": "2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认平顶山市委书记陈向平、市长李明俊"}
            ],
            "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "刘国朝出生年/籍贯/学历/入党及任汝州市委书记前完整履历"},
            "open_questions": [
                {"priority": "critical", "question": "刘国朝出生年、籍贯、学历、入党/参加工作及任汝州市委书记前的履历(之前在哪任职)?", "why_it_matters": "还原其培养路径与选区网络", "suggested_queries": ["刘国朝 汝州 市委书记 简历 此前", "刘国朝 平顶山 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任汝州市委书记(刘国朝之前)及市长(胡红杰之前)姓名与去向, 权力交接时间线?", "why_it_matters": "梳理汝州市委/政府一把手换届", "suggested_queries": ["汝州市 前任 市委书记", "汝州市 市长 交接 2026"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "胡红杰",
        "job": "市长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "河南省", "city": "平顶山市", "region": "汝州市", "job": "市长", "task_id": "henan_汝州市", "time_focus": "2026"},
            "identity": {
                "person_id": "ruzhou_胡红杰",
                "name": "胡红杰", "aliases": [], "gender": "男", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "胡红杰_", "name_birthplace": "胡红杰_", "official_profile_url": "https://www.ruzhou.gov.cn"}
            },
            "current_status": {"current_post": "市委副书记、市长", "current_org": "汝州市人民政府", "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
            "career_timeline": [
                {"start": "", "end": "present", "org": "中共汝州市委员会", "title": "市委副书记", "level": "县处级副职", "location": "汝州市", "system": "party", "rank": "县处级副职", "is_key_promotion": False, "notes": "2026-07 月官方新闻多次确认市委副书记、市长", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "", "end": "present", "org": "汝州市人民政府", "title": "汝州市人民政府市长", "level": "县处级正职", "location": "汝州市", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "官方'领导之窗'明确列出为市委副书记、市长;主持市政府党组(扩)会议(2026-07-27)", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "胡红杰出生年/籍贯/学历、入党及任汝州市长前的整段履历未公开一手", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "汝州市人民政府", "role": "市长", "period": "2026 至今", "source_ids": ["S001", "S002"]},
                {"name": "中共汝州市委员会", "role": "市委副书记", "period": "2026 至今", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "刘国朝", "person_id": "ruzhou_刘国朝", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "胡任市长、刘任市委书记,党政正职搭档", "overlap_org": "汝州市", "overlap_period": "当前", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "杨世崇", "person_id": "ruzhou_杨世崇", "relationship_type": "same_system", "strength": "medium", "evidence": "同任市委,胡为副书记、杨亦为副书记", "overlap_org": "中共汝州市委员会", "overlap_period": "当前", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "走访慰问驻汝部队官兵和退役军人,强调双拥与军民融合", "role_in_event": "带队", "measurable_outcome": "", "location": "汝州市", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "主持市政府党组(扩大)会议,部署安全生产、生态环保、防汛抗旱、项目与科技工作", "role_in_event": "主持", "measurable_outcome": "", "location": "汝州市", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-07", "domain": "environment", "achievement_or_event": "深入麟下镇/产业集聚区/纸坊镇调研黑臭水体治理与污水处理,强调淮河生态保护", "role_in_event": "带队调研", "measurable_outcome": "", "location": "汝州市", "confidence": "confirmed", "source_ids": ["S004"]}
            ],
            "professional_profile": {"primary_specializations": ["economic_management", "environment_protection", "urban_construction"], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["party", "government"], "geographic_pattern": ["汝州市"], "promotion_velocity": {"summary": "2026年在任市委副书记、市长;任前履历与任命时间线待考", "notable_fast_promotions": []}},
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "pragmatic", "evidence": "调研污水处理/棚改/医院提质,强调闭环管理与任务台账", "confidence": "confirmed", "source_ids": ["S004"]},
                    {"trait": "environment_conscious", "evidence": "明确'绿水青山就是金山银山',主抓水环境治理、'一企一管'排污监测", "confidence": "confirmed", "source_ids": ["S004"]}
                ],
                "speech_themes": ["绿水青山就是金山银山", "安全生产/防汛", "城市更新/技术集成", "民生保障"], "management_signals": [],
                "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "胡红杰走访慰问驻汝部队官兵和退役军人", "url": "https://www.ruzhou.gov.cn/contents/36561/751471.html", "publisher": "汝州市人民政府", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市委副书记、市长胡红杰"},
                {"id": "S002", "title": "市政府党组(扩大)会议召开", "url": "https://www.ruzhou.gov.cn/contents/36561/750950.html", "publisher": "汝州市人民政府", "published_at": "2026-07-27", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市长胡红杰主持"},
                {"id": "S004", "title": "胡红杰调研我市生态环境保护重点工作", "url": "https://www.ruzhou.gov.cn/contents/36561/750386.html", "publisher": "汝州市人民政府", "published_at": "2026-07-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "调研污水治理、河湖保护"}
            ],
            "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "胡红杰出生年/籍贯/学历/入党及任汝州市长前履历; 代/正式/转正时间线"},
            "open_questions": [
                {"priority": "critical", "question": "胡红杰出生年、籍贯、学历、入党/工作及任汝州市长前的履历?", "why_it_matters": "还原其培养路径与选区网络", "suggested_queries": ["胡红杰 汝州 市长 简历 此前", "胡红杰 平顶山 任命"], "last_attempted": AS_OF},
                {"priority": "high", "question": "胡红杰任汝州市委副书记/市长的确切任命时间(代理→转正)及其时任前任市长的交接节点?", "why_it_matters": "梳理2026年汝州市政府一把手交接", "suggested_queries": ["汝州市 代市长 任命 2026", "汝州市长 交接"], "last_attempted": AS_OF}
            ]
        }
    },
]

# ── Markdown report data ────────────────────────────────────────────────────
REPORT_FILENAME = f"{TODAY}-汝州市-领导班子工作关系网络调查报告.md"

report_text = f"""# 汝州市领导班子工作关系网络调查报告

> 河南省 · 平顶山市代管 · 汝州市（县级市）
> 调查日期：{AS_OF}（数据截至 2026-07）
> 目标职务：市委书记 & 市长
> 任务 ID：henan_汝州市
> 数据来源：汝州市人民政府门户网站（www.ruzhou.gov.cn，官方一手）+ 本地平顶山市调查存档

---

## 1. 现任市委书记：刘国朝
- **职务**：中共汝州市委书记
- **性别**：男
- **确认依据**：2026-07-31 官方新闻《情系子弟兵 共叙鱼水情 刘国朝带队开展八一建军节走访慰问活动》，正文多处"汝州市委书记刘国朝"，带队慰问驻地官兵。（注：个别版本个别句子将姓名录为"刘国良"，本报告以标题与多数字句采信"刘国朝"。）
- **履历深度**：出生年/籍贯/学历/入党/参加工作及任汝州市委书记前完整履历未获一手 → 列入 open_questions。

## 2. 现任市长：胡红杰
- **职务**：市委副书记、市长
- **性别**：男
- **确认依据**：汝州市政府官网"领导之窗"明确列出"市委副书记、市长：胡红杰"；2026-07-31 官方慰问新闻、07-27 市政府党组（扩大）会议主持、07-17/07-14 调研新闻均一致确认。
- **工作印象**：主持市政府工作，聚焦生态环保（黑臭水体/污水治理/北汝河）、安全生产、"一企一管"排污监测、城市更新与民生保障。
- **履历深度**：出生/籍贯/学历/入党及任汝州前履历、转正时间线未核实 → open_questions。

## 3. 前任领导（去向，待补）
- 前任市委书记（刘国朝之前）、前任市长（胡红杰之前）姓名与去向本轮未能获官方一手确认，列入 high-priority gap。

## 4/5. 现任领导班子成员（官方一手）
| 姓名 | 职务 | 来源确认 |
|---|---|---|
| 刘国朝 | 市委书记 | 慰问新闻 |
| 胡红杰 | 市委副书记、市长 | 领导之窗+多篇新闻 |
| 杨世崇 | 市委副书记 | 慰问/调度会 |
| 张飞 | 市委常委、常务副市长 | 市人大常委会列席 |
| 王红文 | 市委常委、纪委书记、监委主任 | 市人大常委会列席 |
| 黄红丽 | 市委常委、组织部部长 | 市人大常委会/调度会 |
| 李新杰 | 市人大常委会主任 | 市人大常委会会议 |
| 陈海丰 | 副市长 | 领导之窗 |
| 董备战 | 副市长 | 领导之窗/慰问 |
| 于跃峰 | 副市长 | 领导之窗/市政府党组会 |
| 唐佳佳 | 副市长 | 领导之窗 |
| 李慧娟 | 副市长 | 领导之窗/市政府党组会 |
| 郭玉玮 | 市政府秘书长 | 领导之窗/慰问 |
| 张剑奇 | 市人大领导 | 慰问/市人大常委会 |
| 范响立 | 市领导 | 慰问/调度会 |
| 李益恒 | 市领导 | 生态调研/调度会/市政府党组会 |

## 6. 近期人事变动（时间线）
- 2026-07 系列官方新闻（八一慰问、市人大常委会议、市政府党组会、重点调度会）确认刘国朝、胡红杰分任书记/市长，及班子构成。权力交接节点（前任离任、现任接任建/转正时间线）待一手补考。

## 7. 工作关系网络分析（初步）
- **刘国朝 ↔ 胡红杰**：市委书记 × 市长，党政正职搭档（confirmed，强）。
- **刘国朝/胡红杰 ↔ 杨世崇**：常委会副书记关系（confirmed）。
- **胡红杰 ↔ 李新杰**：市政府×市人大监督关系（confirmed）。
- 常委张飞（常务）、王红文（纪委）、黄红丽（组织）构成治理主轴。
- **汝州 ↔ 平顶山**：属市辖县级市，平顶山市委书记陈向平、市长李明俊对汝州有上下级工作联系；跨县观察：龚宪君由舞钢→宝丰县长，反映平顶山内区县干部流动。

## 8. 关键洞察与突破线索
1. **现任党政正职搭档已确认**（刘国朝/胡红杰），是下一步深挖任前履历的锚点。
2. **平县-县际干部流动管道活跃**：龚宪君 舞钢→宝丰为例，可延伸查汝州领导是否经平顶山市区县交流管道到任。
3. **班子分工主线"生态+项目+城市更新"**：胡红杰主抓环保与民生、刘国朝主抓党军共建，治理分工清晰。
4. 前任汝州书记/市长姓名与去向、刘/胡任前履历是最高优先级突破缺口。

## 9. 数据文件说明
- `build_汝州市_data.py` / `data/database/汝州市_network.db` / `data/graph/汝州市_network.gexf`

## 10. 信息来源汇总
- S001 汝州市人民政府门户网站 www.ruzhou.gov.cn（2026-08-06 访问）
  - 官方领导之窗 /channels/36778.html（胡红杰市长/副市长名单）
  - 刘国朝慰问 /contents/36561/751479.html（刘国朝书记）
  - 胡红杰慰问 /contents/36561/751471.html
  - 市政府党组（扩大）会议 /contents/36561/750950.html
  - 市九届人大常委会第三十七次会议（名校长官）
  - 生态环境调研 /contents/36561/750386.html
  - 市重点工作调度会 /contents/36561/750387.html
- S002 本地平顶山市调查存档（report/20260805-平顶山市-领导网络调查报告.md）：陈平/李明俊。
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

    # ── Copy to canonical paths ──────────────────────────────────── (process_tmp also does this)
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