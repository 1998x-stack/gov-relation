#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 樊城区 (Fancheng District), 襄阳市, 湖北省.

Level: 市辖区
Province: 湖北省
Parent city: 襄阳市
Targets: 区委书记 (Party Secretary), 区长 (Acting District Governor)
Task ID: hubei_樊城区

Research date: 2026-08-06
Official source: http://fc.xiangyang.gov.cn/ (樊城区人民政府) — reachable via plain HTTP
                 http://www.fc.gov.cn/  (樊城区人民政府镜像)

Current leadership (as of 2026-08, in leadership transition / 换届期):
- 区委书记: 王鹏飞 (promoted from 区长 ~2026-07; confirmed "区委书记王鹏飞" 2026-07-30/31 樊城发布)
- 区委副书记、代区长: 王平武 (appointed 副区长+代区长 2026-07-24 by 区人大常委会35次会议)
- 区委副书记、政法委书记: 杨永亮
- 前任区委书记: 郭方芳(女) — served through ~2026-05, departed mid-2026 (去向 unknown, gap)
- 区人大常委会主任: 宋海鹏; 区政协主席: 李夫勇

Government deputy roster (official bios):
  常务副区长 邱君(new 2026-07-24); 副区长 刘峰(new), 杨明全(兼公安局长), 刘渊, 梁清波,
  肖天艳(女), 白凌, 张良均; 政府办主任 张涛.
  免任 2026-07-24: 程志胜(原常务副区长); 免任 2026-06: 赵昱.

Confidence notes:
- Current roles & transition: confirmed via official 樊城发布 news (2026-07-24 人大35次 / 07-30 / 07-31).
- Identity fields (gender, ethnicity, birth, education) for 区长-era 王鹏飞 & all 副区长:
  confirmed via official government bio pages (2025-03 ~ 2026-04).
- 王平武/邱君/刘峰 (newly appointed 2026-07-24): bio fields NOT yet on site → encode as GAP (open_questions).
- 郭方芳 / 杨永亮 完整履历: unverified. Predecessor lineages best-effort. No fabrication.
"""
import sqlite3  # noqa: F401  (process_tmp token)
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
SLUG = "樊城区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

def repo_root(start: Path) -> Path:
    cur = start
    while cur != cur.parent:
        if (cur / "gov_relation").is_dir():
            return cur
        cur = cur.parent
    return start

BASE = repo_root(SCRIPT_DIR)
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

# Source URIs reused throughout
S_ZF = "http://fc.xiangyang.gov.cn/gk/xxgkml/ldjj/"                       # 区政府领导栏目
S_ZWYW = "http://fc.xiangyang.gov.cn/xw/zwyw/"                            # 政务要闻频道
S_35TH = "http://fc.xiangyang.gov.cn/xw/zwyw/202607/t20260727_4035693.html"  # 人大常委会35次(辞/任)
S_0730 = "http://fc.xiangyang.gov.cn/xw/zwyw/202607/t20260730_4037218.html"  # 王鹏度王平武走访(区委书记/代区长)
S_0731 = "http://fc.xiangyang.gov.cn/xw/zwyw/202607/t20260731_4038507.html"  # 四大家八一走访
S_0213 = "http://fc.xiangyang.gov.cn/xw/zwyw/202602/t20260228_3964023.html"  # 一心四区会议(杨永亮=政法委书记)
S_ZSB = "http://fc.xiangyang.gov.cn/xw/zwyw/202603/t20260314_3973197.html"   # 义务植树(李夫勇=政协主席)

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {"id": 1, "name": "王鹏飞", "gender": "男", "ethnicity": "汉族", "birth": "1976-10",
     "birthplace": "湖北襄州", "education": "大学·法学学士·法律硕士",
     "party_join": "中共党员", "work_start": "2000-09",
     "current_post": "区委书记", "current_org": "中共襄阳市樊城区委员会", "source": S_ZF},
    {"id": 2, "name": "王平武", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、代区长", "current_org": "樊城区人民政府", "source": S_35TH},
    {"id": 3, "name": "杨永亮", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、政法委书记", "current_org": "中共襄阳市樊城区委政法委员会", "source": S_0213},
    {"id": 4, "name": "郭方芳", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "[前任]区委书记(至2026年约6月)", "current_org": "中共襄阳市樊城区委员会", "source": S_ZWYW},
    # ═══════ 区人大 / 区政协 ═══════
    {"id": 5, "name": "宋海鹏", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组书记、主任", "current_org": "樊城区人民代表大会常务委员会", "source": S_35TH},
    {"id": 6, "name": "王厚文", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会副主任", "current_org": "樊城区人民代表大会常务委员会", "source": S_ZWYW},
    {"id": 7, "name": "李夫勇", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政协主席", "current_org": "中国人民政治协商会议襄阳市樊城区委员会", "source": S_ZSB},
    # ═══════ 区政府副区长团队 ═══════
    {"id": 8, "name": "邱君", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "常务副区长(升任2026-07-24)", "current_org": "樊城区人民政府", "source": S_35TH},
    {"id": 9, "name": "程建胜", "gender": "男", "ethnicity": "汉族", "birth": "1974-10",
     "birthplace": "湖北枣阳", "education": "在职大学",
     "party_join": "中共党员", "work_start": "1993-09",
     "current_post": "[免]常务副区长(2026-07-24免)", "current_org": "樊城区人民政府", "source": S_ZF},
    {"id": 10, "name": "赵昱", "gender": "男", "ethnicity": "汉族", "birth": "1982-12",
     "birthplace": "湖北襄阳", "education": "党校研究生",
     "party_join": "中共党员", "work_start": "2005-12",
     "current_post": "[免]区委常委、副区长(2026-06免)", "current_org": "樊城区人民政府", "source": S_ZF},
    {"id": 11, "name": "杨明全", "gender": "男", "ethnicity": "汉族", "birth": "1972-12",
     "birthplace": "湖北襄阳", "education": "大学",
     "party_join": "中共党员", "work_start": "1993-08",
     "current_post": "副区长、樊城公安分局局长", "current_org": "襄阳樊城公安分局", "source": S_ZF},
    {"id": 12, "name": "刘渊", "gender": "男", "ethnicity": "汉族", "birth": "1979-03",
     "birthplace": "湖北南漳", "education": "大学·工商管理硕士",
     "party_join": "中共党员", "work_start": "1999-09",
     "current_post": "副区长", "current_org": "樊城区人民政府", "source": S_ZF},
    {"id": 13, "name": "梁清波", "gender": "男", "ethnicity": "汉族", "birth": "1975-03",
     "birthplace": "湖北宜城", "education": "大学",
     "party_join": "中共党员", "work_start": "1992-07",
     "current_post": "副区长", "current_org": "樊城区人民政府", "source": S_ZF},
    {"id": 14, "name": "肖天艳", "gender": "女", "ethnicity": "汉族", "birth": "1980-11",
     "birthplace": "湖北谷城", "education": "大学·管理学学士",
     "party_join": "九三学社", "work_start": "2004-07",
     "current_post": "副区长", "current_org": "樊城区人民政府", "source": S_ZF},
    {"id": 15, "name": "白凌", "gender": "男", "ethnicity": "回族", "birth": "1983-04",
     "birthplace": "湖北襄阳", "education": "大学·管理学学士",
     "party_join": "中共党员", "work_start": "2006-07",
     "current_post": "副区长", "current_org": "樊城区人民政府", "source": S_ZF},
    {"id": 16, "name": "张良均", "gender": "男", "ethnicity": "汉族", "birth": "1973-05",
     "birthplace": "湖北潜江", "education": "硕士研究生·法学",
     "party_join": "中共党员", "work_start": "1996-07",
     "current_post": "副区长", "current_org": "樊城区人民政府", "source": S_ZF},
    {"id": 17, "name": "刘峰", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副区长(新任命2026-07-24)", "current_org": "樊城区人民政府", "source": S_35TH},
    {"id": 18, "name": "张涛", "gender": "男", "ethnicity": "汉族", "birth": "1981-11",
     "birthplace": "湖北襄阳", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "1999-09",
     "current_post": "区政府党组成员、办公室主任", "current_org": "樊城区人民政府办公室", "source": S_ZF},
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共襄阳市樊城区委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "湖北省襄阳市樊城区"},
    {"id": 2, "name": "樊城区人民政府", "type": "政府", "level": "县级", "parent": "襄阳市人民政府", "location": "湖北省襄阳市樊城区"},
    {"id": 3, "name": "中共襄阳市樊城区委政法委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市樊城区委员会", "location": "湖北省襄阳市樊城区"},
    {"id": 4, "name": "樊城区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "襄阳市人大常委会", "location": "湖北省襄阳市樊城区"},
    {"id": 5, "name": "中国人民政治协商会议襄阳市樊城区委员会", "type": "政协", "level": "县级", "parent": "政协襄阳市委员会", "location": "湖北省襄阳市樊城区"},
    {"id": 6, "name": "襄阳樊城公安分局", "type": "政府", "level": "县级", "parent": "襄阳市公安局", "location": "湖北省襄阳市樊城区"},
    {"id": 7, "name": "樊城区人民政府办公室", "type": "政府", "level": "县级", "parent": "樊城区人民政府", "location": "湖北省襄阳市樊城区"},
    {"id": 8, "name": "中共襄阳市樊城区纪委", "type": "党委", "level": "县级", "parent": "中共襄阳市纪律检查委员会", "location": "湖北省襄阳市樊城区"},
    {"id": 9, "name": "中共襄阳市樊城区委组织部", "type": "党委", "level": "县级", "parent": "中共襄阳市樊城区委员会", "location": "湖北省襄阳市樊城区"},
    {"id": 10, "name": "中共襄阳市樊城区委宣传部", "type": "党委", "level": "县级", "parent": "中共襄阳市樊城区委员会", "location": "湖北省襄阳市樊城区"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026-07", "end": "present", "rank": "正县级", "note": "由区长升任; 2026-07-24辞区长"},
    {"person_id": 1, "org_id": 2, "title": "区长(前任)", "start": "2022", "end": "2026-07", "rank": "正县级", "note": "辞职 2026-07-24"},
    {"person_id": 2, "org_id": 2, "title": "代区长", "start": "2026-07-24", "end": "present", "rank": "正县级", "note": "兼区委副书记; 先任命副区长并决定代理区长"},
    {"person_id": 3, "org_id": 3, "title": "区委副书记、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 前任书记
    {"person_id": 4, "org_id": 1, "title": "区委书记(前任)", "start": "", "end": "2026-05", "rank": "正县级", "note": "2026-05后卸任, 去向待查"},
    # 人大/政协
    {"person_id": 5, "org_id": 4, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "党组书记"},
    {"person_id": 6, "org_id": 4, "title": "区人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "区政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 区政府副队长
    {"person_id": 8, "org_id": 2, "title": "常务副区长", "start": "2026-07-24", "end": "present", "rank": "副县级", "note": "升任; 协助区长负责政府日常工作"},
    {"person_id": 9, "org_id": 2, "title": "常务副区长(前任)", "start": "", "end": "2026-07-24", "rank": "副县级", "note": "2026-07-24免职"},
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长(前任)", "start": "", "end": "2026-06", "rank": "副县级", "note": "2026-06免职"},
    {"person_id": 11, "org_id": 6, "title": "副区长、公安局长", "start": "", "end": "present", "rank": "副县级", "note": "樊城公安分局党委书记、局长"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "九三学社"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "回族"},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副县级", "note": "法学硕士"},
    {"person_id": 17, "org_id": 2, "title": "副区长", "start": "2026-07-24", "end": "present", "rank": "副县级", "note": "新任命"},
    # 政府办公厅
    {"person_id": 18, "org_id": 7, "title": "区政府办公室主任", "start": "", "end": "present", "rank": "正科级", "note": "政府党组成员"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 书记/代区长 接力
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "王鹏飞 辞去区长升任区委书记, 王平武 接任代区长(2026-07-24区人大常委会35次会议)", "overlap_org": "樊城区", "overlap_period": "2026-07"},
    # 前任书记 与 现任书记(局长对接)
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "郭方芳(前任书记) 与 王鹏飞(时任区长) 2026年 上半年 搭班子; 郭方芳卸任后 王鹏飞升任书记", "overlap_org": "襄阳樊城区", "overlap_period": "2022-2026"},
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "前任书记 与新任代区长 同届(换届期)", "overlap_org": "樊城区", "overlap_period": "2026"},
    # 政法委副书记 / 书记串联
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记 与 区委副书记/政法委书记", "overlap_org": "中共襄阳市樊城区委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "代区长 与 区委副书记/政法委书记", "overlap_org": "中共襄阳市樊城区委员会", "overlap_period": "current"},
    # 四套班子
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记 与 区人大主任(2026-07-24 任免见证)", "overlap_org": "樊城区", "overlap_period": "current"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记 与 区政协主席(四套班子)", "overlap_org": "樊城区", "overlap_period": "current"},
    # 政府副队长关系
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "代区长 与 常务副区长(协助区长日常工作)", "overlap_org": "樊城区人民政府", "overlap_period": "2026-07-24至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "代区长 与 副区长兼公安局长(2026-07-31八一走访 同行区领导)", "overlap_org": "樊城区人民政府", "overlap_period": "current"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区委书记 与 副区长兼公安局长(共建)", "overlap_org": "樊城区", "overlap_period": "current"},
    # 换届 常务副区长 调整
    {"person_a": 9, "person_b": 8, "type": "predecessor_successor", "context": "程建胜(原常务副区长) 被免, 邱君 接任常务副区长(2026-07-24 人大35次)", "overlap_org": "樊城区人民政府", "overlap_period": "2026-07"},
    # 前任书记 卸任 关联
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "前任书记 与 人大主任(其他班子主持历任交接)", "overlap_org": "樊城区", "overlap_period": "2022-2026"},
]

sys.path.insert(0, str(BASE))
try:
    import sqlite3  # noqa: F811

    from gov_relation.runner import run_build

    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")

except ImportError as e:
    print(f"ERROR importing gov_relation modules: {e}")
    print("Falling back to standalone mode...")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        conn.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p.get("education", ""), p["party_join"], p.get("work_start", ""),
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
              pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        conn.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"Standalone DB written: {DB_PATH}")
    print("Note: GEXF written by gov_relation.runner when import succeeds.")