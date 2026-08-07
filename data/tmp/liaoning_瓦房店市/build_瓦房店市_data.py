#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 瓦房店市 (Wafangdian), 大连市, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_瓦房店市
Level: 县级市
Targets: 市委书记 & 市长

Primary source: official 瓦房店市人民政府网站 www.dlwfd.gov.cn (leadership bios + 市委/人大/政协全会报道).
See data/tmp/liaoning_瓦房店市/checkpoint_01_research.md for full source mapping.

Confirmed (2026-08, official):
  - 市委书记 赵东（大连副市长兼；大连长兴岛经开区党工委书记）2026 接任（前任马英骥 2025-12 前兼人大主任）
  - 市长 孙宗（市委副书记、市长、市政府党组书记；兼大连长兴岛经开区党工委副书记、管委会主任）
  - 市委副书记 马明；常务副市长 王占林；副市长 徐晓东/刘春阳(挂职)/黄显刚/王俊(兼公安)/周帅
  - 人大主任 马英骥(2025底)；政协主席 赵迎春；监委主任 朱阿男；法院院长 杨鹏飞；组织部长 仲昭军
Cross-region network (prior/neighbor overlaps, from local repo data): 张延松/杨海三（更任瓦房店副书记，现普兰店/西岗）、
  宋家宝（省工信厅挂职瓦房店市委常委副市长→双塔区长）、周振雷（前任瓦房店市长约2019-2022）。
Open gaps: 宣传部长、政法委书记、纪委书记独立头衔、及多数成人履历细节待核。
"""

import sqlite3
import sys
from pathlib import Path

# Resolve repo root for gov_relation import regardless of run location (staging vs promoted).
_anchor = Path(__file__).resolve().parent
for _d in (_anchor, _anchor.parent, _anchor.parent.parent, _anchor.parent.parent.parent, _anchor.parent.parent.parent.parent):
    if (_d / "gov_relation").is_dir():
        sys.path.insert(0, str(_d))
        break

from gov_relation.runner import run_build

TODAY = "20260806"
AS_OF = "2026-08-06"
SLUG = "瓦房店市"
SRC = "瓦房店市政府官网 https://www.dlwfd.gov.cn/xxgk/szzc/sunzong/"

# Staging paths (DB/GEXF land beside the script)
TMP = Path(__file__).parent.resolve()
DB_PATH = TMP / f"{SLUG}_network.db"
GEXF_PATH = TMP / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────
# id: integer (schema requires INTEGER PK). Org ids start at 100 to avoid collision.

persons = [
    {"id": 1, "name": "赵东", "gender": "男", "ethnicity": "汉族", "birth": "1972年1月", "birthplace": "",
     "education": "在职研究生学历，工商管理硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "大连市人民政府副市长、瓦房店市委书记、大连长兴岛经开区党工委书记",
     "current_org": "大连市人民政府 / 中共瓦房店市委员会 / 大连长兴岛经开（长兴岛经济区）",
     "source": "https://www.dl.gov.cn/col/col11565/index.html + 瓦房店市委常委会报道(id=30212)"},
    {"id": 2, "name": "孙宗", "gender": "男", "ethnicity": "汉族", "birth": "1971年8月", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "中共瓦房店市委副书记、市长、市政府党组书记；大连长兴岛经开区党工委副书记、管委会主任",
     "current_org": "瓦房店市人民政府 / 大连长兴岛经济技术开发区", "source": SRC},
    {"id": 3, "name": "马明", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共瓦房店市委副书记", "current_org": "中共瓦房店市委员会",
     "source": "瓦房政协十届五次会议报道 id=29419"},
    {"id": 4, "name": "马英骥", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "瓦房店市人大常委会主任（曾任市委书记兼，2025-12前）",
     "current_org": "瓦房店市人大常委会", "source": "瓦房市十届人大六次会议 id=29431"},
    {"id": 5, "name": "王占林", "gender": "男", "ethnicity": "满族", "birth": "1970年5月", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、常务副市长、市政府党组副书记", "current_org": "瓦房店市人民政府",
     "source": "https://www.dlwfd.gov.cn/xxgk/szzc/wangzong/resume/"},
    {"id": 6, "name": "徐晓东", "gender": "男", "ethnicity": "汉族", "birth": "1980年2月", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "瓦房店市人民政府",
     "source": "https://www.dlwfd.gov.cn/xxgk/szzc/xxd/resume/"},
    {"id": 7, "name": "刘春阳", "gender": "男", "ethnicity": "汉族", "birth": "1985年5月", "birthplace": "",
     "education": "研究生（挂职干部）", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长（挂职）", "current_org": "瓦房店市人民政府",
     "source": "https://www.dlwfd.gov.cn/xxgk/szzc/liuchunyang/resume/"},
    {"id": 8, "name": "黄显刚", "gender": "男", "ethnicity": "满族", "birth": "1976年4月", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "瓦房店市人民政府",
     "source": "https://www.dlwfd.gov.cn/xxgk/szzc/huangxg/resume/"},
    {"id": 9, "name": "王俊", "gender": "男", "ethnicity": "汉族", "birth": "1974年4月", "birthplace": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长、市公安局党委书记、局长", "current_org": "瓦房店市人民政府 / 瓦房店市公安局",
     "source": "https://www.dlwfd.gov.cn/xxgk/szzc/wangjun/resume/"},
    {"id": 10, "name": "周帅", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长（兼市规划局、林业局局长）", "current_org": "瓦房店市人民政府",
     "source": "https://www.dlwfd.gov.cn/xxgk/szzc/zhoushuai/resume/"},
    {"id": 11, "name": "仲昭军", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、组织部长", "current_org": "中共瓦房店市委员会",
     "source": "高机关党建述职会议 id=27775"},
    {"id": 12, "name": "朱阿男", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市监察委员会主任（2025-12-30当选；现行体制下通常兼任市委常委、纪委书记）",
     "current_org": "瓦房店市监察委员会", "source": "人大十届六次会议 id=29431"},
    {"id": 13, "name": "赵迎春", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政协主席", "current_org": "政协瓦房店市委员会",
     "source": "政协十届五次会议 id=29419/29430"},
    {"id": 14, "name": "杨鹏飞", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市人民法院院长（2025-12-30当选）", "current_org": "瓦房店市人民法院",
     "source": "人大九届六次会议 id=29431"},
    {"id": 15, "name": "张延松", "gender": "男", "ethnicity": "汉", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "普兰店区委副书记、区长（前瓦房店区委副书记）", "current_org": "大连市普兰店区人民政府",
     "source": "data/persons/20260725-辽宁省-大连市-区长-张延松.json"},
    {"id": 16, "name": "杨海三", "gender": "男", "ethnicity": "汉族", "birth": "1977年", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "大连市西岗区委书记（前瓦房店市委副书记）", "current_org": "中共大连市西岗区委员会",
     "source": "data/persons/20260725-辽宁省-大连市-区委书记-杨海三.json"},
    {"id": 17, "name": "宋家宝", "gender": "男", "ethnicity": "汉", "birth": "1981年11月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "朝阳市双塔区委副书记、区长（曾任省工信厅处长挂职瓦房店市委常委副市长）",
     "current_org": "朝阳市双塔区人民政府",
     "source": "data/persons/20260725-辽宁省-朝阳市-双塔区长-宋家宝.json"},
    {"id": 18, "name": "周振雷", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任瓦房店市长（约2019-2022），现大连市长大职级方向待核",
     "current_org": "瓦房店市人民政府（历史）", "source": "张延松档案 id=S003/S005"},
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 100, "name": "中共瓦房店市委员会", "type": "party", "level": "县级", "parent": "大连市", "location": "大连市瓦房店市"},
    {"id": 101, "name": "瓦房店市人民政府", "type": "government", "level": "县级", "parent": "大连市人民政府", "location": "大连市瓦房店市"},
    {"id": 102, "name": "瓦房店市人大常委会", "type": "人大", "level": "县级", "parent": "大连市人大常委会", "location": "大连市瓦房店市"},
    {"id": 103, "name": "政协瓦房店市委员会", "type": "政协", "level": "县级", "parent": "政协辽宁省委员会", "location": "大连市瓦房店市"},
    {"id": 104, "name": "瓦房店市监察委员会", "type": "govt", "level": "县级", "parent": "大连市监察委员会", "location": "大连市瓦房店市"},
    {"id": 105, "name": "瓦房店市公安局", "type": "government", "level": "县级", "parent": "瓦房店市人民政府", "location": "大连市瓦房店市"},
    {"id": 106, "name": "大连市人民政府", "type": "government", "level": "副省级", "parent": "辽宁省人民政府", "location": "大连市"},
    {"id": 107, "name": "中共大连市委", "type": "party", "level": "副省级", "parent": "辽宁省", "location": "大连市"},
    {"id": 108, "name": "大连长兴岛经济技术开发区", "type": "development_zone", "level": "国家级开发区", "parent": "大连市", "location": "大连市长兴岛"},
    {"id": 109, "name": "中共大连市西岗区委员会", "type": "party", "level": "县级", "parent": "中共大连市委", "location": "大连市西岗区"},
    {"id": 110, "name": "大连市普兰店区人民政府", "type": "government", "level": "县级", "parent": "大连市人民政府", "location": "大连市普兰店区"},
    {"id": 111, "name": "朝阳市双塔区人民政府", "type": "government", "level": "县级", "parent": "朝阳市人民政府", "location": "朝阳市双塔区"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 赵东 (1)
    {"person_id": 1, "org_id": 100, "title": "中共瓦房店市委书记", "start_date": "2026年（约前半年）", "end_date": "present", "rank": "正处级(兼副厅)", "note": "由马英骥手中接管，大连副市长兼"},
    {"person_id": 1, "org_id": 106, "title": "大连市人民政府副市长、党组成员", "start_date": "已知不晚于2024年", "end_date": "present", "rank": "副厅级", "note": "兼瓦房店书记"},
    {"person_id": 1, "org_id": 108, "title": "大连长兴岛经开区（长兴岛经济区）党工委书记", "start_date": "已知不晚于2024年", "end_date": "present", "rank": "", "note": "与瓦房店书记多职兼任"},
    # 孙宗 (2)
    {"person_id": 2, "org_id": 100, "title": "市委副书记", "start_date": "现任", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "市长、市政府党组书记", "start_date": "现任", "end_date": "present", "rank": "正处级", "note": "主持政府全面工作，兼管审计"},
    {"person_id": 2, "org_id": 108, "title": "大连长兴岛经开区党工委副书记、管委会主任", "start_date": "现任", "end_date": "present", "rank": "", "note": "与瓦房店市长跨安排"},
    # 马明 (3)
    {"person_id": 3, "org_id": 100, "title": "市委副书记", "start_date": "截至2025-12", "end_date": "present", "rank": "正处级", "note": ""},
    # 马英骥 (4)
    {"person_id": 4, "org_id": 102, "title": "市人大常委会主任", "start_date": "截至2025-12", "end_date": "present", "rank": "正处级", "note": "曾任市委书记兼"},
    {"person_id": 4, "org_id": 100, "title": "市委书记（兼任人大主任）", "start_date": "任期至2025-12前后", "end_date": "2026年初", "rank": "", "note": "2025-12报道中以市委书记兼人大主任身份出现；后由赵东接任书记"},
    # 王占林 (5)
    {"person_id": 5, "org_id": 101, "title": "常务副市长、市政府党组副书记", "start_date": "现任", "end_date": "present", "rank": "正处级", "note": "协助市长"},
    # 徐晓东 (6)
    {"person_id": 6, "org_id": 101, "title": "副市长", "start_date": "现任", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘春阳 (7)
    {"person_id": 7, "org_id": 101, "title": "副市长（挂职）", "start_date": "现任", "end_date": "present", "rank": "副处级", "note": "挂职干部，来自省直"},
    # 黄显刚 (8)
    {"person_id": 8, "org_id": 101, "title": "副市长", "start_date": "现任", "end_date": "present", "rank": "副处级", "note": ""},
    # 王俊 (9)
    {"person_id": 9, "org_id": 101, "title": "副市长", "start_date": "现任", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 105, "title": "市公安局党委书记、局长", "start_date": "现任", "end_date": "present", "rank": "副处级", "note": ""},
    # 周帅 (10)
    {"person_id": 10, "org_id": 101, "title": "副市长（兼规划局、林业局局长）", "start_date": "现任", "end_date": "present", "rank": "副处级", "note": ""},
    # 仲昭军 (11)
    {"person_id": 11, "org_id": 100, "title": "市委常委、组织部长", "start_date": "截至2025-02", "end_date": "present", "rank": "正处级", "note": ""},
    # 朱阿男 (12)
    {"person_id": 12, "org_id": 104, "title": "市监察委员会主任", "start_date": "2025-12-30", "end_date": "present", "rank": "正处级", "note": "现行体制下通常兼任纪委书记"},
    # 赵迎春 (13)
    {"person_id": 13, "org_id": 103, "title": "市政协主席", "start_date": "截至2025-12", "end_date": "present", "rank": "正处级", "note": ""},
    # 杨鹏飞 (14)
    {"person_id": 14, "org_id": 106, "title": "市人民法院院长", "start_date": "2025-12-30", "end_date": "present", "rank": "", "note": ""},
    # 张延松 (15)
    {"person_id": 15, "org_id": 100, "title": "原市委副书记", "start_date": "约2023", "end_date": "约2024", "rank": "正处级", "note": "后任普兰店区区长"},
    {"person_id": 15, "org_id": 110, "title": "普兰店区委副书记、区长", "start_date": "2025", "end_date": "present", "rank": "正处级", "note": ""},
    # 杨海三 (16)
    {"person_id": 16, "org_id": 100, "title": "市委副书记", "start_date": "约2018", "end_date": "2020", "rank": "正处级", "note": "后任西岗区委书记"},
    {"person_id": 16, "org_id": 109, "title": "西岗区委书记", "start_date": "2024-12", "end_date": "present", "rank": "正处级", "note": ""},
    # 宋家宝 (17)
    {"person_id": 17, "org_id": 100, "title": "市委常委、副市长（挂职）", "start_date": "约2021-2023", "end_date": "约2023", "rank": "副处级", "note": "省工信厅处长下派"},
    {"person_id": 17, "org_id": 111, "title": "双塔区委副书记、区长", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": ""},
    # 周振雷 (18)
    {"person_id": 18, "org_id": 101, "title": "市长", "start_date": "约2019-2022", "end_date": "约2022", "rank": "正处级", "note": "前市长，去向待核"},
]

# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记（马明）上下级", "overlap_org": "中共瓦房店市委", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记与常务副市长上下级", "overlap_org": "瓦房店市委/市政府", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长与常务副市长工作搭伴", "overlap_org": "瓦房店市政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "马英骥曾任市委书记(至2025底，兼人大主任)，赵东2026年接任书记", "overlap_org": "中共瓦房店市委", "overlap_period": "2025-2026交接", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "书记赵东与市长孙宗搭班", "overlap_org": "瓦房店市委/市政府", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "predecessor_successor", "context": "周振雷任瓦房店市长约2019-2022，孙宗为现任市长", "overlap_org": "瓦房店市政府", "overlap_period": "约2022", "confidence": "plausible"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "孙宗（市长、市委副书记）与张延松（前市委副书记约2023-2024）同届班子", "overlap_org": "中共瓦房店市委", "overlap_period": "2023-2026（张延松2024离任）", "confidence": "plausible"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "杨海三任瓦房店副书记约2018-2020，孙宗后任市长；时间有间隔", "overlap_org": "瓦房店市委", "overlap_period": "间隔", "confidence": "plausible"},
    {"person_a": 11, "person_b": 3, "type": "same_system", "context": "同任瓦房店市委常委（组织部长、副书记）", "overlap_org": "中共瓦房店市委", "overlap_period": "2023-2025", "confidence": "confirmed"},
    {"person_a": 13, "person_b": 12, "type": "same_system", "context": "政协主席与监委主任同届四套班子", "overlap_org": "瓦房店市", "overlap_period": "2025-", "confidence": "plausible"},
    {"person_a": 6, "person_b": 7, "type": "same_system", "context": "同为副市长（常务班子）", "overlap_org": "瓦房店市政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 9, "type": "same_system", "context": "黄显刚、王俊同为副市长、党组成员", "overlap_org": "瓦房店市政府", "overlap_period": "当前", "confidence": "confirmed"},
    {"person_a": 15, "person_b": 16, "type": "same_system", "context": "均任过瓦房店市委副书记（张2023-2024、杨2018-2020）", "overlap_org": "瓦房店市委", "overlap_period": "有间隔", "confidence": "plausible"},
    {"person_a": 18, "person_b": 15, "type": "same_system", "context": "周振雷任市长2019-2022与张副书记有间歇及班子交集", "overlap_org": "瓦房店市", "overlap_period": "2019-2024", "confidence": "plausible"},
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "宋家宝曾挂职瓦房市委常委副市长与赵东同域", "overlap_org": "瓦房店市", "overlap_period": "约2021-2023", "confidence": "plausible"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG, persons=persons, organizations=organizations,
        positions=positions, relationships=relationships,
        db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True,
    )
    print(f"Ok: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")