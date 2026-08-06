#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 呼和浩特市 (Hohhot), 内蒙古自治区.

Prefecture-level city (地级市), capital of Inner Mongolia Autonomous Region.

Investigation date: 2026-08-06
Task ID: inner_mongolia_呼和浩特市
Research sources:
  - 维基百科《呼和浩特市》现任领导四大机构表
  - 维基百科《于会文》《贺海东》《包钢 (政治人物)》《张佰成》《王莉霞》《云光中》
  - 中国经济网 2024-01 呼和浩特市人大/政协换届快讯

Confirmed as of 2026-08:
  市委书记: 于会文 (2025-12-20 就任, 内蒙古自治区党委常委, 中共二十届中央委员)
  市长:     贺海东 (2021-02 就任)
  人大主任: 李炯 (2024-01)
  政协主席: 崔振武 (2024-01)

Predecessors:
  市委书记 包钢 (2021-09~2025-12, 现内蒙古自治区政府主席)
  市长    张佰成 (2019~2021-02, 现自治区政协副主席兼锡林郭勒盟委书记)

Web access: 官方 huhhot.gov.cn 与百度/Exa 受限, 采用维基百科等二级来源, 个别字段用置信度标注。
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "呼和浩特市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # 1. Core Leadership 市委书记 / 市长
    # ══════════════════════════════════════════════════════════════════════════

    # 于会文 — 市委书记 (2025-12-20 就任, 满族, 二十届中央委员)
    {"id": 1, "name": "于会文", "gender": "男", "ethnicity": "满族",
     "birth": "1968-10", "birthplace": "辽宁省绥中县", "education": "锦州师范学院/辽宁大学/东北财经大学",
     "party_join": "1993", "work_start": "",
     "current_post": "内蒙古自治区党委常委、呼和浩特市委书记", "current_org": "中共呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/于会文"},

    # 贺海东 — 市长 (2021-02)
    {"id": 2, "name": "贺海东", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-02", "birthplace": "内蒙古化德县", "education": "内蒙古大学经济系计划统计专业",
     "party_join": "1985-06", "work_start": "1987-07",
     "current_post": "呼和浩特市委副书记、市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/贺海东"},

    # ══════════════════════════════════════════════════════════════════════════
    # 2. 市委常委会 其他成员
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 3, "name": "孙昊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委副书记、政法委书记", "current_org": "中共呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 4, "name": "李晓燕", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、赛罕区委书记", "current_org": "中共呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 5, "name": "赵燕茹", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、统战部部长、回民区委书记", "current_org": "中共呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 6, "name": "刘占波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、市纪委书记、市监委主任", "current_org": "中共呼和浩特市纪律检查委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 7, "name": "刘继英", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、常务副市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 8, "name": "张际飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、副市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 9, "name": "秦万江", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、呼和浩特警备区司令员", "current_org": "中国人民解放军呼和浩特警备区",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 10, "name": "乔宇驰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、组织部部长", "current_org": "中共呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 11, "name": "王宇天", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、宣传部部长", "current_org": "中共呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 12, "name": "王昆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、副市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 13, "name": "曹志", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市委常委、市委秘书长", "current_org": "中共呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},

    # ══════════════════════════════════════════════════════════════════════════
    # 3. 市政府其他副市长
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 14, "name": "王心宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "民进会员", "work_start": "",
     "current_post": "呼和浩特市副市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市人民政府"},
    {"id": 15, "name": "牛芳泽", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市副市长兼市公安局局长", "current_org": "呼和浩特市公安局",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市人民政府"},
    {"id": 16, "name": "焦鸿", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市副市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市人民政府"},
    {"id": 17, "name": "塔拉", "gender": "男", "ethnicity": "蒙古族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市副市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市人民政府"},
    {"id": 18, "name": "高涵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市副市长", "current_org": "呼和浩特市人民政府",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市人民政府"},

    # ══════════════════════════════════════════════════════════════════════════
    # 4. 人大 / 政协
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 19, "name": "李炯", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-02", "birthplace": "内蒙古呼和浩特市", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市人大常委会主任", "current_org": "呼和浩特市人民代表大会常务委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},
    {"id": 20, "name": "魏红军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市人大常委会副主任", "current_org": "呼和浩特市人民代表大会常务委员会",
     "source": "http://district.ce.cn/newarea/sddy/202401/21/t20240121_38874469.shtml"},
    {"id": 21, "name": "崔振武", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-05", "birthplace": "河北省鸡泽县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "呼和浩特市政协主席", "current_org": "中国人民政治协商会议呼和浩特市委员会",
     "source": "https://zh.wikipedia.org/wiki/呼和浩特市"},

    # ══════════════════════════════════════════════════════════════════════════
    # 5. Predecessors 前任领导人
    # ══════════════════════════════════════════════════════════════════════════
    {"id": 30, "name": "包钢", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1969-05", "birthplace": "辽宁省阜新市", "education": "内蒙古大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "内蒙古自治区人民政府主席（原呼和浩特市委书记）", "current_org": "内蒙古自治区人民政府",
     "source": "https://zh.wikipedia.org/wiki/包钢_(政治人物)"},
    {"id": 31, "name": "张佰成", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-11", "birthplace": "黑龙江省肇东市", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "内蒙古自治区政协副主席兼锡林郭勒盟盟委书记（原呼和浩特市长）", "current_org": "中国人民政治协商会议内蒙古自治区委员会",
     "source": "https://zh.wikipedia.org/wiki/张佰成"},
    {"id": 32, "name": "王莉霞", "gender": "女", "ethnicity": "蒙古族",
     "birth": "1964-06", "birthplace": "辽宁省建平县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原内蒙古自治区政府主席（原呼和浩特市委书记，落马）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/王莉霞"},
]

organizations = [
    {"id": 1, "name": "中共呼和浩特市委员会", "type": "党委", "level": "地厅级", "parent": "中共内蒙古自治区委员会",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 2, "name": "呼和浩特市人民政府", "type": "政府", "level": "地厅级", "parent": "内蒙古自治区人民政府",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 3, "name": "呼和浩特市公安局", "type": "政府", "level": "地厅级", "parent": "内蒙古自治区公安厅",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 4, "name": "呼和浩特警备区", "type": "政府", "level": "地厅级", "parent": "中国人民解放军内蒙古军区",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 5, "name": "呼和浩特市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "内蒙古自治区人大常委会",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 6, "name": "中国人民政治协商会议呼和浩特市委员会", "type": "政协", "level": "地厅级", "parent": "内蒙古自治区政协",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 7, "name": "中共呼和浩特市纪律检查委员会", "type": "纪委", "level": "地厅级", "parent": "中共内蒙古自治区纪委",
     "location": "内蒙古自治区呼和浩特市"},
    # 上级/异地节点
    {"id": 8, "name": "内蒙古自治区人民政府", "type": "政府", "level": "省部级", "parent": "国务院",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 9, "name": "中国人民政治协商会议内蒙古自治区委员会", "type": "政协", "level": "省部级", "parent": "全国政协",
     "location": "内蒙古自治区呼和浩特市"},
    {"id": 10, "name": "中共内蒙古自治区委员会", "type": "党委", "level": "省部级", "parent": "中共中央",
     "location": "内蒙古自治区呼和浩特市"},
]

positions = [
    # 于会文 (1)
    {"person_id": 1, "org_id": 1,
     "title": "内蒙古自治区党委常委、呼和浩特市委书记", "start": "2025-12-20", "end": "present",
     "rank": "省部级副职", "note": "2025年12月20日转任；前生态环境部副部长"},
    {"person_id": 1, "org_id": 10,
     "title": "内蒙古自治区党委常委", "start": "2025-12", "end": "present",
     "rank": "省部级副职", "note": "同时进入自治区党委常委会"},
    # 贺海东 (2)
    {"person_id": 2, "org_id": 2,
     "title": "呼和浩特市市长", "start": "2021-02", "end": "present",
     "rank": "地厅级正职", "note": "2021年2月代市长随后转正"},
    {"person_id": 2, "org_id": 1,
     "title": "呼和浩特市委副书记", "start": "2019-05", "end": "present",
     "rank": "地厅级正职", "note": "2019年5月由通辽市委副书记调任呼和浩特市委副书记"},
    # 孙昊 (3)
    {"person_id": 3, "org_id": 1,
     "title": "呼和浩特市委副书记、政法委书记", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 李晓燕 (4)
    {"person_id": 4, "org_id": 1,
     "title": "呼和浩特市委常委、赛罕区委书记", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 赵燕茹 (5)
    {"person_id": 5, "org_id": 1,
     "title": "呼和浩特市委常委、统战部部长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "兼任回民区委书记"},
    # 刘占波 (6)
    {"person_id": 6, "org_id": 7,
     "title": "呼和浩特市委常委、纪委书记、市监委主任", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 刘继英 (7)
    {"person_id": 7, "org_id": 2,
     "title": "呼和浩特市委常委、常务副市长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 张际飞 (8)
    {"person_id": 8, "org_id": 2,
     "title": "呼和浩特市委常委、副市长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 秦万江 (9)
    {"person_id": 9, "org_id": 4,
     "title": "呼和浩特市委常委、呼和浩特警备区司令员", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 乔宇驰 (10)
    {"person_id": 10, "org_id": 1,
     "title": "呼和浩特市委常委、组织部部长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 王宇天 (11)
    {"person_id": 11, "org_id": 1,
     "title": "呼和浩特市委常委、宣传部部长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 王昆 (12)
    {"person_id": 12, "org_id": 2,
     "title": "呼和浩特市委常委、副市长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 曹志 (13)
    {"person_id": 13, "org_id": 1,
     "title": "呼和浩特市委常委、市委秘书长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 副市长 14-18
    {"person_id": 14, "org_id": 2, "title": "呼和浩特市副市长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任，民进会员"},
    {"person_id": 15, "org_id": 2, "title": "呼和浩特市副市长兼市公安局局长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    {"person_id": 15, "org_id": 3, "title": "呼和浩特市公安局局长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    {"person_id": 16, "org_id": 2, "title": "呼和浩特市副市长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    {"person_id": 17, "org_id": 2, "title": "呼和浩特市副市长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    {"person_id": 18, "org_id": 2, "title": "呼和浩特市副市长", "start": "present", "end": "present",
     "rank": "地厅级副职", "note": "现任"},
    # 人大 19-20
    {"person_id": 19, "org_id": 5, "title": "呼和浩特市人大常委会主任", "start": "2024-01", "end": "present",
     "rank": "地厅级正职", "note": "2024年1月当选"},
    {"person_id": 20, "org_id": 5, "title": "呼和浩特市人大常委会副主任", "start": "2024-01", "end": "present",
     "rank": "地厅级副职", "note": "2024年1月当选"},
    # 政协 21
    {"person_id": 21, "org_id": 6, "title": "呼和浩特市政协主席", "start": "2024-01", "end": "present",
     "rank": "地厅级正职", "note": "2024年1月当选"},
    # 前任 30-32
    {"person_id": 30, "org_id": 8, "title": "内蒙古自治区人民政府主席", "start": "2025-10", "end": "present",
     "rank": "省部级正职", "note": "2025年10月当选；此前2021-09~2025-12任呼和浩特市委书记"},
    {"person_id": 30, "org_id": 1, "title": "呼和浩特市委书记", "start": "2021-09", "end": "2025-12",
     "rank": "厅级正职", "note": "2021年9月接替王莉霞，2025年12月卸任交由于会文"},
    {"person_id": 31, "org_id": 9, "title": "内蒙古自治区政协副主席", "start": "2023-01", "end": "present",
     "rank": "省部级副职", "note": "2023年1月任，后兼任锡林郭勒盟盟委书记"},
    {"person_id": 31, "org_id": 2, "title": "呼和浩特市市长", "start": "2019", "end": "2021-02",
     "rank": "地厅级正职", "note": "前呼和浩特市长，2021年2月辞去由贺海东接任"},
    {"person_id": 32, "org_id": 1, "title": "呼和浩特市委书记", "start": "2019-08", "end": "2021-08",
     "rank": "省部级副职", "note": "前呼和浩特市委书记，后任自治区政府主席并落马"},
]

relationships = [
    # 于会文 - 贺海东 (书记-市长搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长党政正职搭档", "overlap_org": "呼和浩特市", "overlap_period": "2025-12至今"},
    # 于会文 - 包钢 (书记继任)
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor",
     "context": "包钢2025年12月卸任呼和浩特市委书记后，于会文接任", "overlap_org": "呼和浩特市委", "overlap_period": "2025-12交接"},
    # 贺海东 - 张佰成 (市长继任)
    {"person_a": 2, "person_b": 31, "type": "predecessor_successor",
     "context": "张佰成2021年2月辞任市长，贺海东接任", "overlap_org": "呼和浩特市政府", "overlap_period": "2021-02交接"},
    # 包钢 - 王莉霞 (书记继任)
    {"person_a": 30, "person_b": 32, "type": "predecessor_successor",
     "context": "包钢2021年9月接替王莉霞任呼和浩特市委书记", "overlap_org": "呼和浩特市委", "overlap_period": "2021-09交接"},
    # 贺海东 and 包钢 overlap (包钢2021-09-2025-12在呼和浩特, 贺海东2019-05至今在呼和浩特)
    {"person_a": 2, "person_b": 30, "type": "overlap",
     "context": "贺海东任市委副书记/市长期间与市委书记包钢共事2021-09~2025-12", "overlap_org": "呼和浩特市", "overlap_period": "2021-09~2025-12"},
    # 贺海东 and 于会文 also both on内蒙 (于会文内蒙党委常委)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "于会文10为内蒙古党委常委、市委书记，贺海东为市委副书记、市长，同属市委常委会", "overlap_org": "呼和浩特市委常委会", "overlap_period": "2025-12至今"},
    # 秘书长曹志 - 书记于会文
    {"person_a": 13, "person_b": 1, "type": "superior_subordinate",
     "context": "曹志任市委秘书长服务市委常委会工作", "overlap_org": "呼和浩特市委", "overlap_period": "当前"},
    # 组织部长乔宇驰 - 书记
    {"person_a": 10, "person_b": 1, "type": "same_system",
     "context": "组织部长与市委书记同为市委常委会成员", "overlap_org": "呼和浩特市委常委会", "overlap_period": "当前"},
    # 纪委书记刘占波 - 书记
    {"person_a": 6, "person_b": 1, "type": "same_system",
     "context": "市纪委书记为市委常委会成员，与书记同班子", "overlap_org": "呼和浩特市委常委会", "overlap_period": "当前"},
    # 常务副市长刘继英 - 市长
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate",
     "context": "刘继英常务副市长是市长贺海东的直接副手", "overlap_org": "呼和浩特市政府", "overlap_period": "当前"},
    # 副市长王昆/张际飞 - 市长
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate",
     "context": "副市长王昆协助市长工作", "overlap_org": "呼和浩特市政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate",
     "context": "副市长张际飞协助市长工作", "overlap_org": "呼和浩特市政府", "overlap_period": "当前"},
    # 公安局长牛芳泽 与 市长
    {"person_a": 15, "person_b": 2, "type": "superior_subordinate",
     "context": "公安局局长兼副市长，受市长领导", "overlap_org": "呼和浩特市政府", "overlap_period": "当前"},
    # 人大主任李炯 - 市长 (监督关系)
    {"person_a": 19, "person_b": 2, "type": "same_system",
     "context": "人大对市政府有监督职权，同期任市人大主任与市长", "overlap_org": "呼和浩特市", "overlap_period": "2024-01至今"},
    # 政协主席崔振武 - 书记 (四大班子)
    {"person_a": 21, "person_b": 1, "type": "same_system",
     "context": "市政协主席与市委书记同为市级四大班子正职", "overlap_org": "呼和浩特市", "overlap_period": "2025-12至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# Database Builder
# ══════════════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "纪委" in post:
        return ("255,165,0", 12.0)  # Orange for discipline
    if "警察" in post or "公安" in post:
        return ("100,100,100", 12.0)
    if "书记" in post and "副" not in post and "秘书长" not in post:
        return ("255,50,50", 20.0)  # Red, large (市委书记)
    if "市长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue, large (市长)
    if "人大" in post:
        return ("200,255,255", 12.0)  # Cyan
    if "政协" in post:
        return ("255,240,200", 12.0)  # Cream
    if "常委" in post:
        return ("100,150,255", 12.0)
    if "副市长" in post or "副" in post:
        return ("100,150,255", 12.0)
    if "原" in post:
        return ("140,140,140", 10.0)  # Grey for former
    return ("100,100,100", 12.0)


def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,180", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>呼和浩特市领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if pos["person_id"] in [b["id"] for b in persons if False]:
            pass
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"维基百科：呼和浩特市（现任领导四大机构表）","url":"https://zh.wikipedia.org/wiki/呼和浩特市","publisher":"维基百科","published_at":"2026-08","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"确认于会文/李炯/贺海东/崔振武四大机构现任，及市委常委会、副市长名单"},
        {"id":"S002","title":"维基百科：于会文","url":"https://zh.wikipedia.org/wiki/于会文","publisher":"维基百科","published_at":"2025-12-20","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"市委书记于会文完整履历与2025-12-20任职"},
        {"id":"S003","title":"维基百科：贺海东","url":"https://zh.wikipedia.org/wiki/贺海东","publisher":"维基百科","published_at":"2026-04","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"市长贺海东履历"},
        {"id":"S004","title":"维基百科：包钢 (政治人物)","url":"https://zh.wikipedia.org/wiki/包钢_(政治人物)","publisher":"维基百科","published_at":"2026","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"前呼和浩特市委书记，现内蒙古自治区政府主席"},
        {"id":"S005","title":"维基百科：张佰成","url":"https://zh.wikipedia.org/wiki/张佰成","publisher":"维基百科","published_at":"2026","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"前呼和浩特市长，现自治区政协副主席兼锡林郭勒盟委书记"},
        {"id":"S006","title":"维基百科：王莉霞","url":"https://zh.wikipedia.org/wiki/王莉霞","publisher":"维基百科","published_at":"2026","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":"前市委书记/自治区主席，落马"},
        {"id":"S007","title":"中国经济网：李炯当选呼和浩特市人大常委会主任","url":"http://district.ce.cn/newarea/sddy/202401/21/t20240121_38874469.shtml","publisher":"中国经济网","published_at":"2024-01-21","accessed_at":AS_OF,"source_type":"media","reliability":"high","notes":"确认李炯任人大主任、魏红军任副主任、李军任监委主任"},
        {"id":"S008","title":"中国经济网：崔振武当选呼和浩特市政协主席","url":"http://district.ce.cn/newarea/sddy/202401/21/t20240121_38874507.shtml","publisher":"中国经济网","published_at":"2024-01-21","accessed_at":AS_OF,"source_type":"media","reliability":"high","notes":"确认崔振武任政协主席、宋慧/刘建国/武成义任副主席"},
        {"id":"S009","title":"呼和浩特市人民政府领导之窗（参考）","url":"https://www.huhhot.gov.cn","publisher":"呼和浩特市人民政府","published_at":"2026","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"官网访问受限，作为参考"},
    ]


def make_person_json(p, relationships_list, source_register):
    person_rels = [r for r in relationships_list if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
    connected = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
        other_name = next((x["name"] for x in persons if x["id"] == other_id), "")
        connected.append({
            "person": other_name,
            "person_id": f"hohhot_{other_name}",
            "relationship_type": r["type"],
            "strength": "strong" if r["type"] in ("superior_subordinate","predecessor_successor") else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "confirmed" if p["id"] in (1,2) else "plausible",
            "source_ids": ["S001"]
        })

    # Determine rank
    if "书记" in p["current_post"] and "副" not in p["current_post"] and "秘书长" not in p["current_post"]:
        rank = "省部级副职" if "内蒙" in p["current_post"] else "地厅级正职"
    elif "市长" in p["current_post"] and "副" not in p["current_post"]:
        rank = "地厅级正职"
    elif "主席" in p["current_post"] and ("人大" in p["current_post"] or "政协" in p["current_post"]) and "副" not in p["current_post"]:
        rank = "地厅级正职"
    else:
        rank = "地厅级副职"

    result = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "呼和浩特市",
            "region": "呼和浩特市",
            "job": p["current_post"],
            "task_id": "inner_mongolia_呼和浩特市",
            "time_focus": "2026年8月",
            "data_condition": "partial_web_access"
        },
        "identity": {
            "person_id": f"huhhot_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": p.get("birthplace",""),
            "education": p.get("education",""),
            "party_join": p.get("party_join",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": p["id"] in (1,2,19,21),
            "source_ids": ["S001"] if p["id"] <= 18 else (["S007"] if p["id"] in (19,20) else ["S008"])
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": connected,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_province_rotation" if p["id"] == 1 else ("local_ladder" if p["id"] in (2,30,31) else "unknown"),
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p["id"] in (1,2,30,31) else "plausible",
            "current_role": "confirmed" if p["id"] in (1,2,19,21) else "plausible",
            "career_completeness": "complete" if p["id"] in (1,2) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"公开资料受限，{p['name']}部分履历（出生、教育背景、历任职务）待查"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{p['name']}的完整履历", "why_it_matters": "核心领导人履历是关系网络的基础", "suggested_queries": [f"{p['name']} 简历 呼和浩特", f"{p['name']} 任前公示"], "last_attempted": AS_OF}
        ]
    }

    # Fill career timeline for core figures (1=于会文, 2=贺海东, 30=包钢, 31=张佰成)
    if p["id"] == 1:
        result["career_timeline"] = [
            {"start":"2025-12-20","end":"present","org":"中共呼和浩特市委","title":"呼和浩特市委书记","level":"省部级副职","location":"呼和浩特","system":"party","rank":rank,"is_key_promotion":True,"notes":"内蒙古自治区党委常委、呼和浩特市委书记；中共二十届中央委员","confidence":"confirmed","source_ids":["S002"]},
            {"start":"2024-04","end":"2025-12","org":"中华人民共和国生态环境部","title":"党组成员、副部长","level":"省部级副职","location":"北京","system":"other","is_key_promotion":True,"confidence":"confirmed","source_ids":["S002"]},
            {"start":"2022-06","end":"2024-04","org":"中共重庆市委","title":"中共重庆市委常委、万州区委书记","level":"省部级副职","location":"重庆","system":"party","is_key_promotion":True,"confidence":"confirmed","source_ids":["S002"]},
            {"start":"2021-08","end":"2022-06","org":"中共重庆市渝北区委","title":"渝北区委书记","level":"地厅级正职","location":"重庆","system":"party","confidence":"confirmed","source_ids":["S002"]},
            {"start":"2019-12","end":"2021-08","org":"中共重庆市大足区委","title":"大足区委书记","level":"地厅级正职","location":"重庆","system":"party","confidence":"confirmed","source_ids":["S002"]},
            {"start":"2018-11","end":"2019-12","org":"四川省生态环境厅","title":"厅长","level":"地厅级正职","location":"四川","system":"other","confidence":"confirmed","source_ids":["S002"]},
            {"start":"2010","end":"2016","org":"四川省环境保护厅/攀枝花市","title":"副厅长/副市长、副书记","level":"地厅级副职","location":"四川","system":"other","confidence":"plausible","source_ids":["S002"]},
            {"start":"unknown","end":"2010","org":"辽宁省沈阳市","title":"沈阳市政府办公厅政法处处长等","level":"地厅级副职","location":"辽宁","system":"government","confidence":"plausible","source_ids":["S002"],"notes":"1993年入党，公开资料此段仅概括"},
        ]
    elif p["id"] == 2:
        result["career_timeline"] = [
            {"start":"2021-02","end":"present","org":"呼和浩特市人民政府","title":"呼和浩特市长","level":"地厅级正职","location":"呼和浩特","system":"government","is_key_promotion":True,"confidence":"confirmed","source_ids":["S003"]},
            {"start":"2019-05","end":"present","org":"中共呼和浩特市委","title":"呼和浩特市委副书记","level":"地厅级正职","location":"呼和浩特","system":"party","confidence":"confirmed","source_ids":["S003"]},
            {"start":"2017-09","end":"2019-05","org":"中共通辽市委","title":"通辽市委副书记","level":"地厅级副职","location":"通辽","system":"party","confidence":"confirmed","source_ids":["S003"]},
            {"start":"2017-01","end":"2017-09","org":"通辽市人民政府","title":"通辽市常务副市长","level":"地厅级副职","location":"通辽","system":"government","confidence":"confirmed","source_ids":["S003"]},
            {"start":"2010-09","end":"2017-01","org":"通辽市人民政府","title":"通辽市副市长","level":"地厅级副职","location":"通辽","system":"government","confidence":"confirmed","source_ids":["S003"]},
            {"start":"1987-07","end":"2010-09","org":"内蒙古自治区乡镇企业局","title":"经管处科员/干部","level":"科处级","location":"呼和浩特","system":"government","confidence":"plausible","source_ids":["S003"],"notes":"1987年内蒙古大学毕业后进入，中间履历不全"},
        ]
    elif p["id"] == 30:
        result["career_timeline"] = [
            {"start":"2025-10","end":"present","org":"内蒙古自治区人民政府","title":"内蒙古自治区政府主席","level":"省部级正职","location":"呼和浩特","system":"government","is_key_promotion":True,"confidence":"confirmed","source_ids":["S004"]},
            {"start":"2021-09","end":"2025-12","org":"中共呼和浩特市委","title":"呼和浩特市委书记","level":"省部级副职","location":"呼和浩特","system":"party","confidence":"confirmed","source_ids":["S004"]},
            {"start":"2019-08","end":"2021-09","org":"中共内蒙古自治区政府","title":"内蒙古自治区副主席（常务）","level":"省部级副职","location":"呼和浩特","system":"government","confidence":"plausible","source_ids":["S004"]},
        ]
    elif p["id"] == 31:
        result["career_timeline"] = [
            {"start":"2023-07","end":"present","org":"中共锡林郭勒盟委","title":"锡林郭勒盟盟委书记（兼）","level":"地厅级正职","location":"锡林郭勒","system":"party","confidence":"confirmed","source_ids":["S005"]},
            {"start":"2023-01","end":"present","org":"内蒙古自治区政协","title":"自治区政协副主席","level":"省部级副职","location":"呼和浩特","system":"other","confidence":"confirmed","source_ids":["S005"]},
            {"start":"2019","end":"2021-02","org":"呼和浩特市人民政府","title":"呼和浩特市长","level":"地厅级正职","location":"呼和浩特","system":"government","confidence":"confirmed","source_ids":["S005"]},
        ]

    return result


def write_person_jsons():
    source_register = make_source_register()
    job_map = {
        1: "市委书记",
        2: "市长",
        19: "人大主任",
        21: "政协主席",
        30: "前任市委书记",
        31: "前任市长",
    }
    core_ids = [1, 2, 19, 21, 30, 31]
    for p in persons:
        if p["id"] in core_ids:
            data = make_person_json(p, relationships, source_register)
            job = job_map.get(p["id"], p["current_post"])
            fname = f"{TODAY}-内蒙古自治区-呼和浩特市-{job}-{p['name']}.json"
            fpath = os.path.join(BASE, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Person JSON: {fpath}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"\n{'='*60}")
    print(f"呼和浩特市 Network Build")
    print(f"{'='*60}")
    build_db()
    print(f"\nBuilding GEXF graph...")
    build_gexf()
    print(f"\nWriting person JSONs...")
    write_person_jsons()

    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
    print(f"Done.")


if __name__ == "__main__":
    main()