#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 平川区 (Pingchuan District), 白银市, 甘肃省.

Task: gansu_平川区 — 区委书记 & 区长
Province: 甘肃省
Parent city: 白银市
Region: 平川区
Level: 市辖区
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17, from www.bypc.gov.cn 领导之窗):
- 区委书记: 来进明
- 区委副书记、区长: 周春材
- 区委副书记: 刘生福
- 区委常委、组织部部长: 彭晨嘉
- 区委常委、副区长: 陈伟
- 区委常委、政法委书记: 寇志宏
- 区委常委、宣传部部长、兴平街道党工委书记: 朱晓媛
- 区委常委、副区长: 王兴龙
- 区委常委、统战部部长: 吴滨
- 区委常委、区纪委书记、区监委代理主任: 魏晋童
- 区委常委、区人武部部长: 孙胜
- 区政府副区长、市公安局平川分局局长: 王轶明
- 区政府副区长: 闫小东
- 区政府副区长: 杨玉梅
- 区政府副区长(挂职): 李苑
- 区政府副区长: 石福鹏

Sources:
- www.bypc.gov.cn/ldzc/ (official leadership page, accessed 2026-07-17)
"""

import sqlite3
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = SCRIPT_DIR
DB_PATH = os.path.join(STAGING, "平川区_network.db")
GEXF_PATH = os.path.join(STAGING, "平川区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 区委书记 — 来进明
    {
        "id": "pingchuan_lai_jinming",
        "name": "来进明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委书记",
        "current_org": "中共白银市平川区委员会",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "2023年已任平川区委书记（官网页面art_158999a38b6e467bb297db82a5c65d58.html创建于2023年）。2026年7月在任。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 区委副书记、区长 — 周春材
    {
        "id": "pingchuan_zhou_chuncai",
        "name": "周春材",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委副书记、区长",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_4b67ea2a5c464eeeb932f0a146c3acb9.html创建于2024年。2025年12月任区政府党组书记、区长，之前任区委副书记。2026年7月主持区政府第87次常务会议。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ Other Party Standing Committee ══════════════

    # 区委副书记 — 刘生福
    {
        "id": "pingchuan_liu_shengfu",
        "name": "刘生福",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委副书记",
        "current_org": "中共白银市平川区委员会",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_7722f5d5bc4f4da78604ce336905d6cb.html创建于2024年11月。2026年7月在任。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 区委常委、组织部部长 — 彭晨嘉
    {
        "id": "pingchuan_peng_chenjia",
        "name": "彭晨嘉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、组织部部长",
        "current_org": "中共白银市平川区委员会组织部",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_756d20c38fbf4b58bcd8bf083dfec975.html创建于2023年9月。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 区委常委、副区长 — 陈伟
    {
        "id": "pingchuan_chen_wei",
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、副区长",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_af41515a39f64d1685673e9532f074b0.html创建于2026年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 区委常委、政法委书记 — 寇志宏
    {
        "id": "pingchuan_kou_zhihong",
        "name": "寇志宏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、政法委书记",
        "current_org": "中共白银市平川区委员会政法委员会",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_9af37af694cc4989b52faffd1b07db0d.html创建于2024年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 区委常委、宣传部部长、兴平街道党工委书记 — 朱晓媛
    {
        "id": "pingchuan_zhu_xiaoyuan",
        "name": "朱晓媛",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、宣传部部长、兴平街道党工委书记",
        "current_org": "中共白银市平川区委员会宣传部",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_e77e4c86c843446894fdff7ee8bfb963.html创建于2025年。同时兼任兴平街道党工委书记。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 区委常委、副区长 — 王兴龙
    {
        "id": "pingchuan_wang_xinglong",
        "name": "王兴龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、副区长",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_5dd3ca3526844ff99d5dd4d49e874408.html创建于2026年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 区委常委、统战部部长 — 吴滨
    {
        "id": "pingchuan_wu_bin",
        "name": "吴滨",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、统战部部长",
        "current_org": "中共白银市平川区委员会统一战线工作部",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_4490076c868a4f0098b4920b03e1d5bc.html创建于2026年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 区委常委、区纪委书记、区监委代理主任 — 魏晋童
    {
        "id": "pingchuan_wei_jintong",
        "name": "魏晋童",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、区纪委书记、区监委代理主任",
        "current_org": "中共白银市平川区纪律检查委员会",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_7f555222ce1f4b1886798224315f0024.html创建于2026年。代理主任，2026年7月在任。",
        "confidence": "confirmed",
    },

    # 区委常委、区人武部部长 — 孙胜
    {
        "id": "pingchuan_sun_sheng",
        "name": "孙胜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区委常委、区人武部部长",
        "current_org": "白银市平川区人民武装部",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_3249dceba2cc447394bf98a8939a73a2.html创建于2023年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # ══════════════ Government Deputy Leaders ══════════════

    # 副区长、市公安局平川分局局长 — 王轶明
    {
        "id": "pingchuan_wang_yiming",
        "name": "王轶明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区政府副区长、市公安局平川分局局长",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_c5b5e5b541064fa08d60561edd5a547a.html创建于2023年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 副区长 — 闫小东
    {
        "id": "pingchuan_yan_xiaodong",
        "name": "闫小东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区政府副区长",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_6d2d48e5e4b84c44b1a6de8a9132999c.html创建于2024年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 副区长 — 杨玉梅
    {
        "id": "pingchuan_yang_yumei",
        "name": "杨玉梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区政府副区长",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_e3784cbc5fda4e31a2542f4fe8ae35b5.html创建于2026年。2026年7月在任。",
        "confidence": "confirmed",
    },

    # 副区长(挂职) — 李苑
    {
        "id": "pingchuan_li_yuan",
        "name": "李苑",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区政府副区长(挂职)",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_ff2bc999615a41ff871898a67a2a2832.html创建于2025年。挂职副区长，2026年7月在任。",
        "confidence": "confirmed",
    },

    # 副区长 — 石福鹏
    {
        "id": "pingchuan_shi_fupeng",
        "name": "石福鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平川区政府副区长",
        "current_org": "白银市平川区人民政府",
        "source": "www.bypc.gov.cn/ldzc/ (领导之窗)",
        "notes": "官方页面art_6239c72f77b74062a39271058801ade2.html创建于2026年。2026年7月在任。",
        "confidence": "confirmed",
    },
]

organizations = [
    {"id": 1, "name": "中共白银市平川区委员会", "type": "党委", "level": "县处级",
     "parent": "中共白银市委员会", "location": "甘肃省白银市平川区"},
    {"id": 2, "name": "白银市平川区人民政府", "type": "政府", "level": "县处级",
     "parent": "白银市人民政府", "location": "甘肃省白银市平川区"},
    {"id": 3, "name": "中共白银市平川区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "白银市纪委监委", "location": "甘肃省白银市平川区"},
    {"id": 4, "name": "中共白银市平川区委员会组织部", "type": "党委", "level": "县处级",
     "parent": "中共白银市平川区委员会", "location": "甘肃省白银市平川区"},
    {"id": 5, "name": "中共白银市平川区委员会政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共白银市平川区委员会", "location": "甘肃省白银市平川区"},
    {"id": 6, "name": "中共白银市平川区委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共白银市平川区委员会", "location": "甘肃省白银市平川区"},
    {"id": 7, "name": "中共白银市平川区委员会统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共白银市平川区委员会", "location": "甘肃省白银市平川区"},
    {"id": 8, "name": "白银市平川区人民武装部", "type": "党委", "level": "县处级",
     "parent": "白银军分区", "location": "甘肃省白银市平川区"},
    {"id": 9, "name": "白银市公安局平川分局", "type": "政府", "level": "县处级",
     "parent": "白银市公安局", "location": "甘肃省白银市平川区"},
    {"id": 10, "name": "兴平路街道党工委", "type": "党委", "level": "乡科级",
     "parent": "中共白银市平川区委员会", "location": "甘肃省白银市平川区兴平路街道"},
]

positions = [
    # 来进明
    {"person_id": "pingchuan_lai_jinming", "org_id": 1,
     "title": "平川区委书记", "start": "", "end": "present",
     "rank": "副厅级", "note": "2023年官网已有页面记载；2026年7月在任"},

    # 周春材
    {"person_id": "pingchuan_zhou_chuncai", "org_id": 2,
     "title": "平川区委副书记、区长", "start": "", "end": "present",
     "rank": "正县级", "note": "2024年官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_zhou_chuncai", "org_id": 1,
     "title": "平川区委副书记", "start": "", "end": "present",
     "rank": "副厅级", "note": "兼任"},

    # 刘生福
    {"person_id": "pingchuan_liu_shengfu", "org_id": 1,
     "title": "平川区委副书记", "start": "", "end": "present",
     "rank": "副厅级", "note": "2024年11月官网已有页面；2026年7月在任"},

    # 彭晨嘉
    {"person_id": "pingchuan_peng_chenjia", "org_id": 4,
     "title": "平川区委常委、组织部部长", "start": "", "end": "present",
     "rank": "副县级", "note": "2023年9月官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_peng_chenjia", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 陈伟
    {"person_id": "pingchuan_chen_wei", "org_id": 2,
     "title": "平川区委常委、副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "2026年官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_chen_wei", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 寇志宏
    {"person_id": "pingchuan_kou_zhihong", "org_id": 5,
     "title": "平川区委常委、政法委书记", "start": "", "end": "present",
     "rank": "副县级", "note": "2024年官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_kou_zhihong", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 朱晓媛
    {"person_id": "pingchuan_zhu_xiaoyuan", "org_id": 6,
     "title": "平川区委常委、宣传部部长", "start": "", "end": "present",
     "rank": "副县级", "note": "2025年官网已有页面；兼任兴平街道党工委书记；2026年7月在任"},
    {"person_id": "pingchuan_zhu_xiaoyuan", "org_id": 10,
     "title": "兴平街道党工委书记", "start": "", "end": "present",
     "rank": "乡科级", "note": "兼任"},
    {"person_id": "pingchuan_zhu_xiaoyuan", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 王兴龙
    {"person_id": "pingchuan_wang_xinglong", "org_id": 2,
     "title": "平川区委常委、副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "2026年官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_wang_xinglong", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 吴滨
    {"person_id": "pingchuan_wu_bin", "org_id": 7,
     "title": "平川区委常委、统战部部长", "start": "", "end": "present",
     "rank": "副县级", "note": "2026年官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_wu_bin", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 魏晋童
    {"person_id": "pingchuan_wei_jintong", "org_id": 3,
     "title": "平川区委常委、区纪委书记、区监委代理主任", "start": "", "end": "present",
     "rank": "副县级", "note": "2026年官网已有页面；代理主任；2026年7月在任"},
    {"person_id": "pingchuan_wei_jintong", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 孙胜
    {"person_id": "pingchuan_sun_sheng", "org_id": 8,
     "title": "平川区委常委、区人武部部长", "start": "", "end": "present",
     "rank": "副县级", "note": "2023年官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_sun_sheng", "org_id": 1,
     "title": "平川区委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # 王轶明
    {"person_id": "pingchuan_wang_yiming", "org_id": 9,
     "title": "白银市公安局平川分局局长", "start": "", "end": "present",
     "rank": "正县级", "note": "2023年官网已有页面；2026年7月在任"},
    {"person_id": "pingchuan_wang_yiming", "org_id": 2,
     "title": "平川区政府副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "兼任"},

    # 闫小东
    {"person_id": "pingchuan_yan_xiaodong", "org_id": 2,
     "title": "平川区政府副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "2024年官网已有页面；2026年7月在任"},

    # 杨玉梅
    {"person_id": "pingchuan_yang_yumei", "org_id": 2,
     "title": "平川区政府副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "2026年官网已有页面；2026年7月在任"},

    # 李苑
    {"person_id": "pingchuan_li_yuan", "org_id": 2,
     "title": "平川区政府副区长(挂职)", "start": "", "end": "present",
     "rank": "副县级", "note": "2025年官网已有页面；挂职；2026年7月在任"},

    # 石福鹏
    {"person_id": "pingchuan_shi_fupeng", "org_id": 2,
     "title": "平川区政府副区长", "start": "", "end": "present",
     "rank": "副县级", "note": "2026年官网已有页面；2026年7月在任"},
]

relationships = [
    # 来进明 ↔ 周春材 (党政正职搭档)
    {"person_a": "pingchuan_lai_jinming", "person_b": "pingchuan_zhou_chuncai",
     "type": "superior_subordinate", "strength": "strong",
     "context": "来进明作为区委书记，周春材作为区长，为平川区党政正职搭档",
     "overlap_org": "中共白银市平川区委员会/白银市平川区人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 来进明 ↔ 刘生福 (书记-副书记)
    {"person_a": "pingchuan_lai_jinming", "person_b": "pingchuan_liu_shengfu",
     "type": "superior_subordinate", "strength": "strong",
     "context": "来进明作为区委书记，刘生福作为区委副书记，在区委班子共事",
     "overlap_org": "中共白银市平川区委员会",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 来进明 ↔ 其他区委常委 (区委班子共事)
    # Each常委 as区委班子成员
    *[{"person_a": "pingchuan_lai_jinming", "person_b": pid,
       "type": "overlap", "strength": "strong",
       "context": f"来进明作为区委书记，与{name}在区委常委会共事",
       "overlap_org": "中共白银市平川区委员会",
       "overlap_period": "至今", "confidence": "confirmed"}
      for pid, name in [
          ("pingchuan_peng_chenjia", "彭晨嘉"),
          ("pingchuan_chen_wei", "陈伟"),
          ("pingchuan_kou_zhihong", "寇志宏"),
          ("pingchuan_zhu_xiaoyuan", "朱晓媛"),
          ("pingchuan_wang_xinglong", "王兴龙"),
          ("pingchuan_wu_bin", "吴滨"),
          ("pingchuan_wei_jintong", "魏晋童"),
          ("pingchuan_sun_sheng", "孙胜"),
      ]],

    # 周春材 ↔ 区政府副区长 (区政府班子共事)
    *[{"person_a": "pingchuan_zhou_chuncai", "person_b": pid,
       "type": "superior_subordinate", "strength": "strong",
       "context": f"周春材作为区长，与{name}在区政府班子共事",
       "overlap_org": "白银市平川区人民政府",
       "overlap_period": "至今", "confidence": "confirmed"}
      for pid, name in [
          ("pingchuan_chen_wei", "陈伟"),
          ("pingchuan_wang_xinglong", "王兴龙"),
          ("pingchuan_wang_yiming", "王轶明"),
          ("pingchuan_yan_xiaodong", "闫小东"),
          ("pingchuan_yang_yumei", "杨玉梅"),
          ("pingchuan_li_yuan", "李苑"),
          ("pingchuan_shi_fupeng", "石福鹏"),
      ]],
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "区长" in role and "副书记" in role:
        return "50,100,255"
    elif "区长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role or "监委" in role:
        return "255,165,0"
    elif "政法委" in role:
        return "150,100,50"
    elif "人武部" in role:
        return "130,130,130"
    elif "组织部" in role:
        return "180,130,200"
    elif "宣传部" in role:
        return "100,150,200"
    elif "统战部" in role:
        return "200,150,100"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return "区委书记" in role or ("区长" in role and "副书记" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org,
                source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"], p["notes"],
              p["confidence"]))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
              pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength,
                context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")


# ── BUILD GEXF ───────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>平川区领导班子工作关系网络 - 甘肃省白银市平川区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p_{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{p["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o_{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["name"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person - Organization edges (worked_at)
    for pos in positions:
        person = next(p for p in persons if p["id"] == pos["person_id"])
        lines.append(f'      <edge id="e{eid}" source="p_{pos["person_id"]}" target="o_{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person-Person edges (relationship)
    for r in relationships:
        weight = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p_{r["person_a"]}" target="p_{r["person_b"]}" label="{esc(r["context"][:50])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{r["type"]}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")
    print(f"    Person nodes: {len(persons)}")
    print(f"    Organization nodes: {len(organizations)}")
    print(f"    Worked-at edges: {len(positions)}")
    print(f"    Relationship edges: {len(relationships)}")


# ── MAIN ──────────────────────────────────────────────────────

def main():
    print(f"Building 平川区 network data...")
    build_db()
    build_gexf()
    print("Done.")

if __name__ == "__main__":
    main()
