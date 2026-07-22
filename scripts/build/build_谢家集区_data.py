#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 谢家集区 (Xiejiaji District, Huainan, Anhui) leadership network.

谢家集区 — 安徽省淮南市辖区, 淮南市西部, 面积约273平方公里,
辖5街道3镇1乡: 谢家集街道、蔡家岗街道、立新街道、平山街道、
谢三村街道、唐山镇、李郢孜镇、望峰岗镇、孤堆回族乡.
Research date: 2026-07-15

Sources:
  - https://www.xiejiaji.gov.cn/zwgk/ldzc/ (official leadership page, accessed 2026-07-15)
  - https://www.xiejiaji.gov.cn/ (district government news, accessed 2026-07-15)

Confidence: Current leadership roster confirmed from official Xiejiaji government
leadership portal. Career histories sourced from same portal's individual profile pages.
"""

import json
import os
import sqlite3
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_谢家集区")
DB_PATH = os.path.join(STAGING, "谢家集区_network.db")
GEXF_PATH = os.path.join(STAGING, "谢家集区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders (Targets) ──
    # 1. 陈海涛 — 谢家集区委书记
    {"id": 1, "name": "陈海涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-10", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委书记", "current_org": "中共谢家集区委",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "一级调研员。历任潘集区贺疃乡党委副书记、乡长，潘集区政府副区长，大通区政府副区长，田家庵区委常委、副区长、常务副区长，田家庵区委副书记，谢家集区委副书记、区政府区长。",
     "confidence": "confirmed"},

    # 2. 陈亚东 — 谢家集区长
    {"id": 2, "name": "陈亚东", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "", "native_place": "",
     "education": "研究生/法学硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区长", "current_org": "谢家集区人民政府",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "一级调研员。历任淮南市人才工作领导小组办公室主任，八公山区政府副区长，共青团市委书记，谢家集区委副书记（正县）、区委党校校长。",
     "confidence": "confirmed"},

    # ── District Committee Standing Members ──
    # 3. 王立成 — 区委副书记（正县）
    {"id": 3, "name": "王立成", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-12", "birthplace": "", "native_place": "",
     "education": "省委党校研究生/经济学学士、管理学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委副书记、区委党校校长", "current_org": "中共谢家集区委",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "正县级。历任省粮食和物资储备局财务审计处副处长，省粮食和物资储备保障中心主任。",
     "confidence": "confirmed"},

    # 4. 孙寺 — 组织部部长
    {"id": 4, "name": "孙寺", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-07", "birthplace": "", "native_place": "",
     "education": "大学/理学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委、组织部部长", "current_org": "中共谢家集区委组织部",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任淮南市委组织部农村组织科副科长、主任科员，市委非公经济和社会组织工委办公室（党代表联络办公室）主任，市委组织部城市组织科科长，市委组织部组织指导科科长，市委组织部机关党委专职副书记、一级主任科员，市党员电化教育中心主任。",
     "confidence": "confirmed"},

    # 5. 廖欣 — 统战部部长
    {"id": 5, "name": "廖欣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委、统战部部长", "current_org": "中共谢家集区委统战部",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "履历详情待补充。",
     "confidence": "plausible"},

    # 6. 徐明 — 常务副区长
    {"id": 6, "name": "徐明", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-11", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委、常务副区长", "current_org": "谢家集区人民政府",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任杨公镇党委委员，李郢孜镇党委副书记、镇长、党委书记，淮南高新区智造园区党工委书记。",
     "confidence": "confirmed"},

    # 7. 张馨 — 人武部部长
    {"id": 7, "name": "张馨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委、区人武部部长", "current_org": "谢家集区人民武装部",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "现役军人身份，履历详情未公开。",
     "confidence": "plausible"},

    # 8. 王炜 — 区委常委
    {"id": 8, "name": "王炜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委", "current_org": "中共谢家集区委",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "具体职务分工待查。",
     "confidence": "plausible"},

    # 9. 马迪 — 纪委书记
    {"id": 9, "name": "马迪", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-12", "birthplace": "", "native_place": "",
     "education": "大学/经济学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委、纪委书记、监委主任", "current_org": "中共谢家集区纪律检查委员会",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任市纪委副科级纪检监察员、正科级纪检监察员，市纪委党风政风监督室副主任，市纪委监委第六纪检监察室副主任、一级主任科员。",
     "confidence": "confirmed"},

    # 10. 张宇 — 政法委书记
    {"id": 10, "name": "张宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委、政法委书记", "current_org": "中共谢家集区委政法委员会",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任市检察院副科级检察员，市委政法委执法监督室副主任科员、主任科员，市委防范办副主任，市委政法委法治和执法监督科科长、一级主任科员。",
     "confidence": "confirmed"},

    # 11. 李亮 — 区委常委
    {"id": 11, "name": "李亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区委常委", "current_org": "中共谢家集区委",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "具体职务分工待查。",
     "confidence": "plausible"},

    # ── Government Deputy Mayors ──
    # 12. 桂超林 — 副区长（非党）
    {"id": 12, "name": "桂超林", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-08", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "农工党", "work_start": "",
     "current_post": "谢家集区副区长", "current_org": "谢家集区人民政府",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "三级调研员。历任农工党淮南市委办公室副主任、主任，农工党淮南市委专职副主委。",
     "confidence": "confirmed"},

    # 13. 朱峰 — 副区长、公安分局局长
    {"id": 13, "name": "朱峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "", "native_place": "",
     "education": "大学/工学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区副区长、谢家集公安分局局长", "current_org": "淮南市公安局谢家集分局",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "三级高级警长。历任淮南市看守所政委，淮南市公安局毛集分局党委副书记、政委，淮南市公安局经济犯罪侦查支队支队长，淮南市公安局谢家集分局党委书记、局长。",
     "confidence": "confirmed"},

    # 14. 赵佳 — 副区长
    {"id": 14, "name": "赵佳", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-02", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区副区长", "current_org": "谢家集区人民政府",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任大通区九龙岗镇计生办科员，市生态环境局科员、副科长、科长、办公室主任。",
     "confidence": "confirmed"},

    # 15. 李二宝 — 副区长
    {"id": 15, "name": "李二宝", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-04", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区副区长", "current_org": "谢家集区人民政府",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任谢家集区政府办公室副主任，区委组织部副部长、区委非公经济和社会组织工委书记，谢家集区唐山镇党委副书记、镇长，唐山镇党委书记。",
     "confidence": "confirmed"},

    # ── Predecessors ──
    # 16. 陈海涛* — previous 区长 (same person as id 1, listed for position record)
    # (Handled via positions table referencing person_id 1)

    # ──人大 ──
    {"id": 16, "name": "韩涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "1984-07",
     "current_post": "谢家集区人大常委会主任", "current_org": "谢家集区人大常委会",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任寿县双庙小学教师，寿县政府办干事、秘书、副科长、科长、副主任，寿县县委办副主任兼房产局局长、住建局党组书记，寿县政府办主任、党组书记，寿县副县长，寿县县委常委、县委办公室主任、政法委书记，市委副秘书长、市政府副秘书长（兼）、市委信访局局长、市政府信访局党组书记、局长。2024年7月任现职。",
     "confidence": "confirmed"},

    # ──政协 ──
    {"id": 17, "name": "陈玉惠", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "谢家集区政协主席", "current_org": "政协谢家集区委员会",
     "source": "https://www.xiejiaji.gov.cn/zwgk/ldzc/",
     "notes": "历任八公山区团区委副书记、书记，八公山区妇联主席，八公山区教育局党委书记，八公山区委常委、宣传部部长，谢家集区委常委、政法委书记，谢家集区政协主席。",
     "confidence": "confirmed"},
]

organizations = [
    {"id": 1, "name": "中共谢家集区委", "type": "党委", "level": "县级",
     "parent": "中共淮南市委", "location": "安徽省淮南市谢家集区"},
    {"id": 2, "name": "谢家集区人民政府", "type": "政府", "level": "县级",
     "parent": "淮南市人民政府", "location": "安徽省淮南市谢家集区平山路"},
    {"id": 3, "name": "中共谢家集区纪律检查委员会", "type": "纪委", "level": "县级",
     "parent": "中共淮南市纪律检查委员会", "location": "安徽省淮南市谢家集区"},
    {"id": 4, "name": "中共谢家集区委组织部", "type": "党委", "level": "县级",
     "parent": "中共谢家集区委", "location": "安徽省淮南市谢家集区"},
    {"id": 5, "name": "中共谢家集区委统战部", "type": "党委", "level": "县级",
     "parent": "中共谢家集区委", "location": "安徽省淮南市谢家集区"},
    {"id": 6, "name": "中共谢家集区委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共谢家集区委", "location": "安徽省淮南市谢家集区"},
    {"id": 7, "name": "谢家集区人民武装部", "type": "政府", "level": "县级",
     "parent": "淮南军分区", "location": "安徽省淮南市谢家集区"},
    {"id": 8, "name": "淮南市公安局谢家集分局", "type": "政府", "level": "县级",
     "parent": "淮南市公安局", "location": "安徽省淮南市谢家集区"},
    {"id": 9, "name": "谢家集区人大常委会", "type": "人大", "level": "县级",
     "parent": "淮南市人大常委会", "location": "安徽省淮南市谢家集区"},
    {"id": 10, "name": "政协谢家集区委员会", "type": "政协", "level": "县级",
     "parent": "政协淮南市委员会", "location": "安徽省淮南市谢家集区"},
]

positions = [
    # 陈海涛 - 历任
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级", "note": "一级调研员"},
    {"person_id": 1, "org_id": 2, "title": "区长（前任）", "start": "", "end": "", "rank": "正处级", "note": "由谢家集区长升任区委书记"},
    # 潘集区贺疃乡
    {"person_id": 1, "org_id": 1, "title": "潘集区贺疃乡党委副书记、乡长", "start": "", "end": "", "rank": "乡科级", "note": "早期任职"},
    {"person_id": 1, "org_id": 1, "title": "潘集区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "大通区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "田家庵区委常委、副区长、常务副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "田家庵区委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},

    # 陈亚东
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "一级调研员"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "谢家集区委副书记（正县）、区委党校校长", "start": "", "end": "", "rank": "正处级", "note": "前任职务"},
    {"person_id": 2, "org_id": 1, "title": "八公山区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "共青团市委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "淮南市人才工作领导小组办公室主任", "start": "", "end": "", "rank": "正处级", "note": ""},

    # 王立成
    {"person_id": 3, "org_id": 1, "title": "区委副书记、区委党校校长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "省粮食和物资储备局财务审计处副处长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "省粮食和物资储备保障中心主任", "start": "", "end": "", "rank": "正处级", "note": ""},

    # 孙寺
    {"person_id": 4, "org_id": 4, "title": "区委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "淮南市委组织部农村组织科副科长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委非公经济和社会组织工委办公室主任", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委组织部城市组织科科长", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委组织部组织指导科科长", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委组织部机关党委专职副书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市党员电化教育中心主任", "start": "", "end": "", "rank": "正科级", "note": ""},

    # 廖欣
    {"person_id": 5, "org_id": 5, "title": "区委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 徐明
    {"person_id": 6, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "杨公镇党委委员", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "李郢孜镇党委副书记、镇长、党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "淮南高新区智造园区党工委书记", "start": "", "end": "", "rank": "副处级", "note": ""},

    # 张馨
    {"person_id": 7, "org_id": 7, "title": "区委常委、区人武部部长", "start": "", "end": "present", "rank": "副处级", "note": "现役军人"},

    # 王炜
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},

    # 马迪
    {"person_id": 9, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市纪委副科级纪检监察员", "start": "", "end": "", "rank": "乡科级", "note": "副科级"},
    {"person_id": 9, "org_id": 1, "title": "市纪委正科级纪检监察员", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市纪委党风政风监督室副主任", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "市纪委监委第六纪检监察室副主任", "start": "", "end": "", "rank": "正科级", "note": ""},

    # 张宇
    {"person_id": 10, "org_id": 6, "title": "区委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市检察院副科级检察员", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委政法委执法监督室副主任科员、主任科员", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委防范办副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委政法委法治和执法监督科科长", "start": "", "end": "", "rank": "正科级", "note": ""},

    # 李亮
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},

    # 桂超林
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "农工党，三级调研员"},
    {"person_id": 12, "org_id": 1, "title": "农工党淮南市委办公室副主任、主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "农工党淮南市委专职副主委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # 朱峰
    {"person_id": 13, "org_id": 8, "title": "副区长、谢家集公安分局局长", "start": "", "end": "present", "rank": "副处级", "note": "三级高级警长"},
    {"person_id": 13, "org_id": 1, "title": "淮南市看守所政委", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "淮南市公安局毛集分局党委副书记、政委", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "淮南市公安局经济犯罪侦查支队支队长", "start": "", "end": "", "rank": "正科级", "note": ""},

    # 赵佳
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "大通区九龙岗镇计生办科员", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市生态环境局科员、副科长、科长、办公室主任", "start": "", "end": "", "rank": "正科级", "note": ""},

    # 李二宝
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "谢家集区政府办公室副主任", "start": "", "end": "", "rank": "副科级", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "区委组织部副部长、非公经济和社会组织工委书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "谢家集区唐山镇党委副书记、镇长", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "唐山镇党委书记", "start": "", "end": "", "rank": "乡科级", "note": ""},

    # 韩涛（人大主任）
    {"person_id": 16, "org_id": 9, "title": "区人大常委会主任", "start": "2024-07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "寿县双庙小学教师", "start": "1984-07", "end": "1985-03", "rank": "", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "寿县政府办干事、秘书、副科长、科长", "start": "1985-03", "end": "1997-02", "rank": "乡科级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "寿县政府办副主任", "start": "1997-02", "end": "2004-03", "rank": "副科级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "寿县县委办副主任兼房产局局长、住建局党组书记", "start": "2004-03", "end": "2010-08", "rank": "正科级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "寿县政府办主任、党组书记", "start": "2010-08", "end": "2014-12", "rank": "正科级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "寿县副县长", "start": "2014-12", "end": "2016-05", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "寿县县委常委、县委办公室主任、政法委书记", "start": "2016-05", "end": "2021-12", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 16, "org_id": 1, "title": "市委副秘书长、市政府副秘书长（兼）、市委信访局局长", "start": "2021-12", "end": "2024-05", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 9, "title": "区人大常委会党组书记、主任", "start": "2024-07", "end": "present", "rank": "正处级", "note": ""},

    # 陈玉惠（政协主席）
    {"person_id": 17, "org_id": 10, "title": "区政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "八公山区团区委副书记、书记", "start": "", "end": "", "rank": "乡科级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "八公山区妇联主席", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "八公山区教育局党委书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "八公山区委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "谢家集区委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": ""},
]

relationships = [
    # 陈海涛 ↔ 陈亚东 — 区委书记与区长
    {"person_a": 1, "person_b": 2,
     "type": "superior_subordinate",
     "context": "区委书记与区长，前后任区长（陈海涛升任书记后陈亚东接任区长）",
     "overlap_org": "中共谢家集区委",
     "overlap_period": "2025/2026-",
     "confidence": "confirmed"},

    # 陈海涛 ↔ 王立成 — 书记与副书记
    {"person_a": 1, "person_b": 3,
     "type": "superior_subordinate",
     "context": "区委书记与专职副书记",
     "overlap_org": "中共谢家集区委",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 陈亚东 ↔ 徐明 — 区长与常务副区长
    {"person_a": 2, "person_b": 6,
     "type": "superior_subordinate",
     "context": "区长与常务副区长",
     "overlap_org": "谢家集区人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 孙寺（组织部）↔ 陈海涛 — 组织部长与书记
    {"person_a": 4, "person_b": 1,
     "type": "superior_subordinate",
     "context": "组织部部长与区委书记",
     "overlap_org": "中共谢家集区委",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 马迪（纪委）↔ 陈海涛 — 纪委书记与书记
    {"person_a": 9, "person_b": 1,
     "type": "superior_subordinate",
     "context": "纪委书记与区委书记",
     "overlap_org": "中共谢家集区委",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 张宇（政法委）↔ 陈海涛
    {"person_a": 10, "person_b": 1,
     "type": "superior_subordinate",
     "context": "政法委书记与区委书记",
     "overlap_org": "中共谢家集区委",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 陈海涛（曾任区长）→ 陈亚东（接任区长）——前后任
    {"person_a": 1, "person_b": 2,
     "type": "predecessor_successor",
     "context": "陈海涛原为谢家集区长，升任区委书记后陈亚东接任区长",
     "overlap_org": "谢家集区人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 陈玉惠曾与陈海涛共事（谢家集区）
    {"person_a": 17, "person_b": 1,
     "type": "overlap",
     "context": "陈玉惠曾任谢家集区委常委、政法委书记，与陈海涛在区委常委会共事",
     "overlap_org": "中共谢家集区委",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 陈亚东曾在八公山区任职，与陈玉惠有八公山区交集
    {"person_a": 2, "person_b": 17,
     "type": "overlap",
     "context": "陈亚东曾任八公山区副区长，陈玉惠曾任八公山区委常委、宣传部部长，可能曾有交集",
     "overlap_org": "八公山区",
     "overlap_period": "",
     "confidence": "plausible"},

    # 陈海涛跨区经历（潘集→大通→田家庵→谢家集）的转换模式
    # 李二宝成长于谢家集区本地体系
    {"person_a": 15, "person_b": 6,
     "type": "overlap",
     "context": "李二宝（唐山镇党委书记）与徐明（李郢孜镇党委书记）均为乡镇党委书记晋升",
     "overlap_org": "谢家集区",
     "overlap_period": "",
     "confidence": "plausible"},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' for a person node."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post and "政协" not in post:
        return "255,50,50"    # Red — party secretary
    elif "区长" in post or "县长" in post:
        return "50,100,255"   # Blue — government leader
    elif "纪委" in post:
        return "255,165,0"    # Orange — discipline
    elif "人大" in post:
        return "200,255,255"  # Cyan — people's congress
    elif "政协" in post:
        return "255,240,200"  # Cream — political consultative
    else:
        return "100,100,100"  # Grey — other


def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "区长" in post or "县长" in post or "主任" in post or "主席" in post


def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def create_database(db_path):
    """Create SQLite database with persons, organizations, positions, relationships."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
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
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
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
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                native_place, education, party_join, work_start, current_post, current_org,
                source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
              p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""),
              p.get("source", ""), p.get("notes", ""), p.get("confidence", "")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos.get("title", ""),
              pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""),
              pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", ""), r.get("confidence", "")))

    conn.commit()
    conn.close()


def generate_gexf(gexf_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>谢家集区领导班子工作关系网络 — Party Secretary, District Mayor, and leadership team</description>')
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

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at) — only current/main positions
    for pos in positions:
        if pos.get("end") == "present" or pos.get("end") == "":
            eid += 1
            lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos.get("title", ""))}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="worked_at"/>')
            conf = "confirmed"
            lines.append(f'          <attvalue for="2" value="{conf}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(gexf_path) or ".", exist_ok=True)
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── main ─────────────────────────────────────────────────────────────────

def main():
    print(f"=== 谢家集区 Leadership Network Data Builder ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()

    # 1. Database
    print(f"Creating database: {DB_PATH}")
    create_database(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # 2. GEXF
    print(f"\nCreating GEXF: {GEXF_PATH}")
    generate_gexf(GEXF_PATH)
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  GEXF file size: {gexf_size} bytes")

    # 3. Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")

    for p in persons:
        conf = p.get("confidence", "")
        print(f"  - {p['name']}: {p.get('current_post', '')} ({conf})")

    print(f"\nDone. Files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
