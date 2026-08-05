#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 赫章县 (Hezhang County), 毕节市, 贵州省.

Level: 县
Province: 贵州省
Parent city: 毕节市
Targets: 县委书记 & 县长
Task ID: guizhou_赫章县
Investigation date: 2026-08-05

Research sources (primary: 赫章县人民政府门户 www.gzhezhang.gov.cn):
  - 领导之窗·政府领导: https://www.gzhezhang.gov.cn/zwgk/zfxxgkzl/fdzdgknr/jgjj/
      + 历任/现任领导 profiles (/zwgk/ldzc_5980939/202503/t20250327_*.html)
  - 关于公开赫章县党政领导干部、信访部门领导及相关人员分管（负责）工作及联系方式的通告
      https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html
      （完整班子名单 + 职务 + 分管 + 联系电话；官方一手来源）
  - 关于停用原县委书记热线电话的通告 2026-07-13 (领导更替佐证)
  - 政务要闻/县委常委会 news 2026-05 ~ 07

Confidence notes:
  - 刘元刚 (县委书记): confirmed via official 2026-07-06 通告 + 2026-07-28 调研新闻. 前任胡书龙截至
    2026-05-13 仍在任（主持县委常委会，见 202605/t20260515_90176675.html），故书记交接窗口为
    2026-05-13 之后、2026-07-06 之前。刘元刚的出生年、籍贯、教育、任书记前职务未找到（网络受限：
    Exa 限流、百度 403）—— open gap。
  - 袁靓 (县委副书记/县政府党组书记/县长): confirmed via 官方领导之窗 bio + 通告。男，穿青人，
    1983年12月出生，中共党员，大学学历。任县长前的职务路径未找到—— open gap。
  - 县委班子（张俊/李华 副书记；马永江统战、陈敬政法、孟异纪委、朱启辉宣传、张林涛组织 常委；
    老家星/翟超群/李卓君 常委副县长挂职）: confirmed via 官方通告。
  - 县政府班子（刘秋宏/李松松/周燚/徐磊/蒋本旺/陈祖军/付庆梅/周廷/关榆）: confirmed via 官方
    通告 + 领导之窗（出生/学历部分）。
  - 四套班子：张勇 县人大常委会主任、安玲 县政协主席 confirmed via 2026-05-13 县委常委会新闻。
  - 前任县委书记胡书龙卸任去向、前任县长、刘元刚此前履历: 未取得，列为 open gap。
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "赫章县"
TODAY = datetime.now().strftime("%Y%m%d")

# DB + GEXF written into the current directory (staging when run from data/tmp)
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 县委主要领导（一把手／二把手）═══════
    {
        "id": 1,
        "name": "刘元刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共赫章县委书记",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html; https://www.gzhezhang.gov.cn/xwzx/zwyw/202607/t20260729_90670371.html"
    },
    {
        "id": 2,
        "name": "袁靓",
        "gender": "男",
        "ethnicity": "穿青人",
        "birth": "1983年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委副书记、县政府党组书记、县长",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_5980939/202503/t20250327_87291600.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    # ═══════ 县委副书记 ═══════
    {
        "id": 3,
        "name": "张俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委副书记",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 4,
        "name": "李华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委副书记",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html; https://www.gzhezhang.gov.cn/xwzx/zwyw/202605/t20260515_90176675.html"
    },
    # ═══════ 县委常委 ═══════
    {
        "id": 5,
        "name": "马永江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、县委统战部部长",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 6,
        "name": "陈敬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、县委政法委书记",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 7,
        "name": "孟异",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、县纪委书记、县监委主任",
        "current_org": "中共赫章县纪委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 8,
        "name": "朱启辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、县委宣传部部长",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 9,
        "name": "张林涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、县委组织部部长、县直机关工委书记",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 10,
        "name": "李松松",
        "gender": "男",
        "ethnicity": "穿青人",
        "birth": "1983年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、县政府党组副书记、常务副县长",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_59888/202608/t20260803_90689215.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 11,
        "name": "周燚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、副县长",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_5989/202503/t20250327_87291597.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 12,
        "name": "老家星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、副县长（挂职，广州市番禺区对口帮扶）",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 13,
        "name": "翟超群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、副县长（挂职，中央统战部对口帮扶）",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_5989/202503/t20250327_87291593.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 14,
        "name": "李卓君",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1988年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县委常委、副县长（挂职，台盟中央对口帮扶）",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_5989/202603/t20260319_89886802.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    # ═══════ 县政府领导 ═══════
    {
        "id": 15,
        "name": "刘秋宏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "研究生学历，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县政府党组副书记、贵州赫章经济开发区党工委副书记、管委会主任",
        "current_org": "贵州赫章经济开发区",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_5989/202503/t20250327_87291598.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 16,
        "name": "徐磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县政府党组成员、副县长",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 17,
        "name": "蒋本旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县政府党组成员、副县长",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzg_5989/202503/t20250327_87291591.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 18,
        "name": "陈祖军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县政府党组成员、副县长、县公安局党委书记、局长、督查长",
        "current_org": "赫章县公安局",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_5989/202503/t20250327_87291590.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 19,
        "name": "付庆梅",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "1986年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县政府党组成员、副县长",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_5989/202503/t20250327_87291588.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 20,
        "name": "周廷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县政府党组成员、副县长",
        "current_org": "赫章县人民政府",
        "source": "https://www.gzhezhang.gov.cn/zwgk/ldzc_598904/202608/t20260803_90689272.html; https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    {
        "id": 21,
        "name": "关榆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县政府党组成员、县政府办公室党组书记、主任",
        "current_org": "赫章县人民政府办公室",
        "source": "https://www.gzhezhang.gov.cn/xwzx/tzgg/zwgg/202607/t20260706_90591119.html"
    },
    # ═══════ 县人大 / 政协 ═══════
    {
        "id": 22,
        "name": "张勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "赫章县人大常委会主任",
        "current_org": "赫章县人大常委会",
        "source": "https://www.gzhezhang.gov.cn/xwzx/zwyw/202605/t20260515_90176675.html"
    },
    {
        "id": 23,
        "name": "安玲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协赫章县委员会主席",
        "current_org": "政协赫章县委员会",
        "source": "https://www.gzhezhang.gov.cn/xwzx/zwyw/202605/t20260515_90176675.html"
    },
    # ═══════ 前任书记（交接链）═══════
    {
        "id": 24,
        "name": "胡书龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任赫章县委书记（截至2026-05-13在任，2026-07前卸任，去向待查）",
        "current_org": "中共赫章县委",
        "source": "https://www.gzhezhang.gov.cn/xwzx/zwyw/202605/t20260515_90176675.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共赫章县委", "type": "党委", "level": "县级", "parent": "中共毕节市委", "location": "毕节市赫章县"},
    {"id": 2, "name": "赫章县人民政府", "type": "政府", "level": "县级", "parent": "毕节市人民政府", "location": "毕节市赫章县"},
    {"id": 3, "name": "赫章县公安局", "type": "政府", "level": "县级", "parent": "赫章县人民政府", "location": "毕节市赫章县"},
    {"id": 4, "name": "赫章县人大常委会", "type": "人大", "level": "县级", "parent": "毕节市人大常委会", "location": "毕节市赫章县"},
    {"id": 5, "name": "政协赫章县委员会", "type": "政协", "level": "县级", "parent": "政协毕节市委员会", "location": "毕节市赫章县"},
    {"id": 6, "name": "赫章县人民政府办公室", "type": "政府", "level": "县级", "parent": "赫章县人民政府", "location": "毕节市赫章县"},
    {"id": 7, "name": "中共赫章县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共赫章县委", "location": "毕节市赫章县"},
    {"id": 8, "name": "贵州赫章经济开发区", "type": "开发区", "level": "县级", "parent": "赫章县人民政府", "location": "毕节市赫章县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 刘元刚 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共赫章县委书记", "start": "2026-07(约)", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作。经官方 2026-07-06 通告确认在任；2026-07-28 以县委书记调研产业项目。前任胡书龙 2026-05-13 仍在任，交接窗口为 2026-05-13 后、2026-07-06 前。"},
    # 袁靓 — 县长
    {"id": 2, "person_id": 2, "org_id": 1, "title": "赫章县委副书记、县人民政府党组书记", "start": "", "end": "present", "rank": "正处级",
     "note": "兼任县政府党组书记；办公室书记、县长互为 AB 岗（接访排班）。"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "赫章县县长", "start": "", "end": "present", "rank": "正处级",
     "note": "领导县政府全面工作，负责审计、粮食等工作。2026-05 至 08 多次调研教育、招商、产业等工作。"},
    # 县委副书记
    {"id": 4, "person_id": 3, "org_id": 1, "title": "赫章县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "协助县委书记抓党建，负责农业农村、乡村振兴、工青妇等（官方 2026-07-06 通告分管分工）。"},
    {"id": 5, "person_id": 4, "org_id": 1, "title": "赫章县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "协助县委书记抓‘三农’、驻村工作。2026-05-13 县委常委会在列。"},
    # 县委常委
    {"id": 6, "person_id": 5, "org_id": 1, "title": "赫章县委常委、县委统战部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县委统战部全面工作，负责统战、民族、宗教、侨务等。"},
    {"id": 7, "person_id": 6, "org_id": 1, "title": "赫章县委常委、县委政法委书记", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县委政法委全面工作，负责政法、信访维稳、治安综治、消防、依法治县。"},
    {"id": 8, "person_id": 7, "org_id": 7, "title": "赫章县委常委、县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县纪委监委全面工作，负责纪检、监察、巡察、党风廉政。"},
    {"id": 9, "person_id": 8, "org_id": 1, "title": "赫章县委常委、县委宣传部部长", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县委宣传部，负责宣传、意识形态、精神文明建设，联系教育、文旅等。"},
    {"id": 10, "person_id": 9, "org_id": 1, "title": "赫章县委常委、县委组织部部长、县直机关工委书记", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县委组织部，负责组织、党建、人才、机构编制、干部考核等。"},
    {"id": 11, "person_id": 10, "org_id": 2, "title": "赫章县委常委、县政府常务副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责县政府常务工作，分管发改、财政、税务、应急、国资等；协助县长负责审计、粮食。县委常委会成员。"},
    {"id": 12, "person_id": 11, "org_id": 2, "title": "赫章县委常委、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责自然资源（非常规矿）、住建、城管、交通运输、人社等。县委常委会成员。"},
    {"id": 13, "person_id": 12, "org_id": 2, "title": "赫章县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "挂职",
     "note": "挂职副县长，负责广州市番禺区对口帮扶赫章工作。"},
    {"id": 14, "person_id": 13, "org_id": 2, "title": "赫章县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "挂职",
     "note": "挂职副县长，负责中央统战部对口帮扶赫章工作，协助负责项目、乡村振兴、招商、文旅等。"},
    {"id": 15, "person_id": 14, "org_id": 2, "title": "赫章县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "挂职",
     "note": "挂职副县长，负责台盟中央对口帮扶赫章工作，协助负责乡村振兴、教育、卫生、文旅等。"},
    # 县政府领导
    {"id": 16, "person_id": 15, "org_id": 8, "title": "赫章县政府党组副书记、经开区党工委副书记、管委会主任", "start": "", "end": "present", "rank": "兼",
     "note": "负责贵州赫章经济开发区管委会全面工作，负责工业、民营经济、矿产、科技等。"},
    {"id": 17, "person_id": 16, "org_id": 2, "title": "赫章县政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责民政、市场监管、商务、招商引资、营商环境、政务公开等。"},
    {"id": 18, "person_id": 17, "org_id": 2, "title": "赫章县政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责农业农村（乡村振兴、生态移民）、林业、水务、气象、易地搬迁、烤烟等；对接广州番禺帮扶。"},
    {"id": 19, "person_id": 18, "org_id": 2, "title": "赫章县政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管公安、司法、道路交通安全、退役军人事务、国防动员、社会稳定、人防。"},
    {"id": 20, "person_id": 18, "org_id": 3, "title": "赫章县公安局党委书记、局长、督查长", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县公安局全面工作。"},
    {"id": 21, "person_id": 19, "org_id": 2, "title": "赫章县政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责教育、旅游、文旅、文体广电、卫生健康、医疗保障、大健康等。"},
    {"id": 22, "person_id": 20, "org_id": 2, "title": "赫章县政府党组成员、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责能源、电力等工作，分管县能源局。"},
    {"id": 23, "person_id": 21, "org_id": 6, "title": "赫章县政府党组成员、县政府办公室党组书记、主任", "start": "", "end": "present", "rank": "",
     "note": "主持县政府办公室全面工作。"},
    # 四套班子
    {"id": 24, "person_id": 22, "org_id": 4, "title": "赫章县人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": "2026-05-13 出席县委常委会。"},
    {"id": 25, "person_id": 23, "org_id": 5, "title": "政协赫章县委员会主席", "start": "", "end": "present", "rank": "正处级",
     "note": "2026-05-13 出席县委常委会。"},
    # 前任书记
    {"id": 26, "person_id": 24, "org_id": 1, "title": "前任中共赫章县委书记", "start": "（任职起止待查）", "end": "2026（卸任）", "rank": "正处级",
     "note": "截至 2026-05-13 仍在任（主持县委常委会）；2026-07-06 前卸任，由刘元刚接任。卸任去向待查。"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记刘元刚与县长袁靓党政正职搭档，共同主持县委常委会、县委县政府联席会议（2026-07 接手）。", "overlap_org": "中共赫章县委/赫章县政府", "overlap_period": "2026-07"},
    {"id": 2, "person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记领导县委副书记李华（‘三农'/驻村），2026-05 县委常委会同台出席。", "overlap_org": "中共赫章县委", "overlap_period": "2026-05"},
    {"id": 3, "person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记领导县委副书记张俊（党建、乡村振兴、工青妇等）。", "overlap_org": "中共赫章县委", "overlap_period": "2026-07"},
    {"id": 4, "person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记领导县委政法委书记陈敬（政法、综治）。", "overlap_org": "中共赫章县委", "overlap_period": "2026-07"},
    {"id": 5, "person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记领导县纪委书记、监委主任孟异（纪检监察、巡察）。", "overlap_org": "中共赫章县委/县纪委", "overlap_period": "2026-07"},
    {"id": 6, "person_a": 1, "person_b": 10, "type": "上下级", "context": "县委书记领导常务副县长李松松（县委常委会成员）。", "overlap_org": "中共赫章县委/县政府", "overlap_period": "2026-07"},
    {"id": 7, "person_a": 1, "person_b": 22, "type": "同级协作", "context": "县委书记与县人大常委会主任张勇同台出席县委常委会。", "overlap_org": "赫章县四套班子", "overlap_period": "2026-05"},
    {"id": 8, "person_a": 2, "person_b": 10, "type": "上下级", "context": "县长领导常务副县长李松松（协助县长审计、财政）。", "overlap_org": "赫章县人民政府", "overlap_period": "2026-07"},
    {"id": 9, "person_a": 2, "person_b": 15, "type": "上下级", "context": "县长与县政府党组副书记、经开区主任刘秋宏同属县政府班子。", "overlap_org": "赫章县人民政府", "overlap_period": "2026-07"},
    {"id": 10, "person_a": 2, "person_b": 18, "type": "上下级", "context": "县长领导副县长、公安局长陈祖军（政府班子成员）。", "overlap_org": "赫章县人民政府/县公安局", "overlap_period": "2026-07"},
    {"id": 11, "person_a": 1, "person_b": 24, "type": "前继-后继", "context": "刘元刚继胡书龙任赫章县委书记。胡书龙 2026-05-13 仍在任，2026-07 前卸任由刘元刚接任。", "overlap_org": "中共赫章县委", "overlap_period": "2026"},
    {"id": 12, "person_a": 24, "person_b": 2, "type": "上下级", "context": "前任县委书记胡书龙与县长袁靓在 2026-05 县委常委会同台（胡书龙主持）。", "overlap_org": "中共赫章县委/县政府", "overlap_period": "2026-05"},
]

# ── SQLite Build ───────────────────────────────────────────────────────────
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
conn.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
    )
for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )
for pos in positions:
    cur.execute(
        "INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
    )
for r in relationships:
    cur.execute(
        "INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )
conn.commit()

# ── GEXF Generation ────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"
    elif "县长" in post and "副" not in post:
        return "50,100,255"
    elif "常务副县长" in post:
        return "50,120,255"
    elif "纪委书记" in post:
        return "255,165,0"
    elif "副县长" in post:
        return "50,150,255"
    elif "副书记" in post:
        return "255,120,60"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "纪委" in t:
        return "255,220,180"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "开发区" in t:
        return "220,230,180"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return ("书记" in post and "副" not in post) or ("县长" in post and "副" not in post)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Research Agent - gov-relation</creator>')
lines.append('    <description>赫章县领导班子工作关系网络 - 贵州省毕节市</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ── Summary ────────────────────────────────────────────────────────────────
print(f"赫章县 network build complete.")
print(f"  Database:        {DB_PATH} ({DB_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  GEXF:            {GEXF_PATH} ({GEXF_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print()
print("Confidence notes:")
print("  - 刘元刚 (县委书记): confirmed via official 2026-07 通告 + 调研新闻; earlier career empty (gap)")
print("  - 袁靓 (县长):      confirmed via official 领导之窗 bio + 通告")
print("  - 班子成员:         confirmed via official 通告 / 领导之窗 / 县委常委会新闻")
print("  - 前任书记胡书龙交接窗口 confirmed; 去向与履历为 open gap")