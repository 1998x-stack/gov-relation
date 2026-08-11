#!/usr/bin/env python3
"""营口市（辽宁省·地级市）领导班子工作关系网络 - 数据构建脚本

目标职务：市委书记、市长
调查截至：2026-08-06
一手来源：营口市人民政府官网 www.yingkou.gov.cn（市政府领导之窗）、营口市纪检监察网、媒体报道。

数据分级（confidence）：
- confirmed：一手官方来源或两处独立可靠来源
- plausible：可信媒体/百科，部分佐证
- unverified：线索不足，不构成强图边
"""

import sqlite3
import sys
from pathlib import Path

# Allow running from staging dir, scripts/build, or repo root
REPO_ROOT = Path(__file__).resolve()
while not (REPO_ROOT / "gov_relation").is_dir() and REPO_ROOT != REPO_ROOT.parent:
    REPO_ROOT = REPO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

AS_OF = "2026-08-06"
SLUG = "营口市"

# ── 人员数据 ─────────────────────────────────────────────────────────────

persons = [
    # 市委书记
    {
        "id": 1,
        "name": "姚华明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "辽宁省",
        "education": "全日制大学学历（北京外国语大学文学学士）；在职研究生学历（法国巴黎第一大学公共管理硕士）",
        "party_join": "1992年6月",
        "work_start": "1994年7月",
        "current_post": "市委书记",
        "current_org": "中共营口市委",
        "source": "https://r.jina.ai/http://www.yingkou.gov.cn/；搜狗搜索元宝汇总/搜狗百科；中国经济网",
        "notes": "营口军分区党委委员、常委、第一书记；中共辽宁省第十三届委员会委员，辽宁省第十四届、第十四届全国人大代表。2024年5月任市委书记。",
    },
    # 市长
    {
        "id": 2,
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "辽宁省",
        "education": "研究生学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长、市政府党组书记",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001001/002001001003/leader.html",
        "notes": "主持市政府全面工作，分管市审计局。曾任沈阳市苏家屯区委书记、沈阳市委常委、秘书长，2023年3月任沈阳市委常委、常务副市长，2024年5月任营口市委副书记、提名为市长候选人。",
    },
    # 常务副市长
    {
        "id": 3,
        "name": "李进辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-05",
        "birthplace": "",
        "education": "在职研究生学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长、市政府党组副书记",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003022/leader.html",
        "notes": "负责市政府常务工作；分管市发改委、财政局、应急管理局、统计局、信访局等。",
    },
    # 副市长
    {
        "id": 4,
        "name": "韩冰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "全日制研究生学历、经济学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003024/leader.html",
        "notes": "营口市委常委、市人民政府党组成员、副市长。",
    },
    # 副市长（公安局长）
    {
        "id": 5,
        "name": "赵涵斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-09",
        "birthplace": "",
        "education": "大学学历、法学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "营口市公安局",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003016/leader.html",
        "notes": "营口市人民政府党组成员、副市长，市公安局局长。",
    },
    # 副市长
    {
        "id": 6,
        "name": "王正刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市政府党组成员",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003019/leader.html",
        "notes": "分管应急、农业、防汛等工作。",
    },
    # 副市长
    {
        "id": 7,
        "name": "李人杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "",
        "education": "在职研究生学历、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市政府党组成员",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003001/leader.html",
        "notes": "",
    },
    # 市政府党组成员
    {
        "id": 8,
        "name": "王殿丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-12",
        "birthplace": "",
        "education": "研究生学历、管理学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003021/leader.html",
        "notes": "营口市人民政府党组成员。",
    },
    # 副市长（无党派）
    {
        "id": 9,
        "name": "付波",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1975-04",
        "birthplace": "",
        "education": "全日制研究生学历、工学硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003023/leader.html",
        "notes": "无党派人士。",
    },
    # 副市长（挂职）
    {
        "id": 10,
        "name": "高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-03",
        "birthplace": "",
        "education": "在职研究生学历、工程硕士学位，高级工程师",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市政府党组成员（挂职）",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/002001/002001003/002001003025/leader.html",
        "notes": "挂职副市长，高级工程师。",
    },
    # 纪委书记
    {
        "id": 11,
        "name": "胡哲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "营口市纪委监委",
        "source": "http://jwjw.yingkou.gov.cn（营口市纪检监察网 2026-07-23）",
        "notes": "中共营口市第十三届纪律检查委员会书记。副书记：赵连海、韩逢华、王旭；常务会委员：赵本、李先维、戴全力。",
    },
    # 市人大常委会主任
    {
        "id": 12,
        "name": "史卫东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "营口市人大常委会",
        "source": "http://www.ykrd.gov.cn（营口市第十七届人大常委会）",
        "notes": "营口市第十七届人大常委会主任。",
    },
    # 前任市长（姚华明到营的前任）
    {
        "id": 13,
        "name": "许桂清",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任）营口市市长",
        "current_org": "营口市人民政府",
        "source": "中国经济网：姚华明代市长，许桂清辞去市长职务（2021-08）",
        "notes": "2021年姚华明任营口市代市长后 许桂清辞去市长职务。",
    },
    # 前任市委书记（李强）
    {
        "id": 14,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-11",
        "birthplace": "",
        "education": "研究生学历、硕士学位",
        "party_join": "1998年9月",
        "work_start": "1992年8月",
        "current_post": "辽宁省副省长",
        "current_org": "辽宁省人民政府",
        "source": "澎湃新闻：李强升任辽宁省副省长（2024-03）",
        "notes": "营口市委书记（2021年前后—2024年3月），曾在沈阳工作多年，2024年3月升任辽宁省副省长。",
    },
    # 前任市委书记（赵长富，被查）
    {
        "id": 15,
        "name": "赵长富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961-01",
        "birthplace": "",
        "education": "",
        "party_join": "1982年7月",
        "work_start": "1983年8月",
        "current_post": "（均已卸任，被查）",
        "current_org": "中共营口市委",
        "source": "辽宁省纪委监委通报 / 封面新闻",
        "notes": "营口市委原书记，2022年11月主动投案接受审查调查，2023年5月被开除党籍。",
    },
]

# ── 机构数据 ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共营口市委", "type": "党委", "level": "地级市", "parent": "中共辽宁省委", "location": "辽宁省营口市"},
    {"id": 2, "name": "营口市人民政府", "type": "政府", "level": "地级市", "parent": "辽宁省人民政府", "location": "辽宁省营口市"},
    {"id": 3, "name": "营口市公安局", "type": "政府", "level": "地级市部门", "parent": "营口市人民政府", "location": "辽宁省营口市"},
    {"id": 4, "name": "营口市纪委监委", "type": "纪委", "level": "地级市", "parent": "中共营口市委", "location": "辽宁省营口市"},
    {"id": 5, "name": "营口市人大常委会", "type": "人大", "level": "地级市", "parent": "营口市", "location": "辽宁省营口市"},
    {"id": 6, "name": "政协营口市委员会", "type": "政协", "level": "地级市", "parent": "营口市", "location": "辽宁省营口市"},
    {"id": 7, "name": "辽宁省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "辽宁省沈阳市"},
    {"id": 8, "name": "中国银行", "type": "央属企业", "level": "央企", "parent": "中国银行保险监督管理委员会", "location": "北京市"},
]

# ── 任职数据 ─────────────────────────────────────────────────────────────

positions = [
    # 市委书记 姚华明
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-05", "end_date": "present", "rank": "正厅级", "note": "主持市委全面工作；2024-06 起兼营口军分区党委第一书记"},
    {"person_id": 1, "org_id": 1, "title": "市委副书记", "start_date": "2021", "end_date": "2024-05", "rank": "副厅级", "note": "营口市委常委（正厅级）、副书记"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2022-01", "end_date": "2024-05", "rank": "正厅级", "note": "2021年任代市长，2022年1月当选市长"},
    {"person_id": 1, "org_id": 8, "title": "中国银行宁波市分行党委书记、行长", "start_date": "2018", "end_date": "2021", "rank": "", "note": "中国银行深圳分行行长（此前任中国银行北京市分行副行长、中银香港人力资源总经理等）"},
    # 市长李军
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024-05", "end_date": "present", "rank": "正厅级", "note": "兼市长，主持市政府全面工作"},
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "2024-05", "end_date": "present", "rank": "正厅级", "note": "主持市政府全面工作，分管市审计局"},
    # 常务副市长
    {"person_id": 3, "org_id": 2, "title": "常务副市长、市政府党组副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责市政府常务、发改、财税、应急、统计、信访等"},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "在市委常委会任委员"},
    # 副市长
    {"person_id": 4, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "营口市委常委、副市长"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管公安、司法、社会稳定"},
    {"person_id": 5, "org_id": 3, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任"},
    {"person_id": 6, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管应急、农业、防汛"},
    {"person_id": 7, "org_id": 2, "title": "副市长、市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "市政府党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "无党派人士"},
    {"person_id": 10, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "挂职，高级工程师"},
    # 纪委
    {"person_id": 11, "org_id": 4, "title": "市纪委书记、市监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "中共营口市第十三届纪律检查委员会书记"},
    # 人大
    {"person_id": 12, "org_id": 5, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "营口市第十七届人大常委会主任"},
    # 前任市长
    {"person_id": 13, "org_id": 2, "title": "市长", "start_date": "", "end_date": "2021", "rank": "正厅级", "note": "姚华明任代市长时辞去"},
    # 前任书记
    {"person_id": 14, "org_id": 1, "title": "市委书记", "start_date": "2021", "end_date": "2024-03", "rank": "正厅级", "note": "后升任辽宁省副省长"},
    {"person_id": 14, "org_id": 7, "title": "副省长", "start_date": "2024-03", "end_date": "present", "rank": "副部级", "note": "辽宁省副省长"},
    # 前任书记（被查）
    {"person_id": 15, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "2022-11 主动投案，2023-05 开除党籍"},
]

# ── 关系数据 ─────────────────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "姚华明（书记）由市长升任书记，李军继任市长；现任党政主官搭档", "overlap_org": "中共营口市委/营口市人民政府", "overlap_period": "2024-至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 14, "type": "predecessor_successor", "context": "姚华明接李强任市委书记；2021届李强任书记时姚任市委副书记/市长", "overlap_org": "中共营口市委", "overlap_period": "2021-2024", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor", "context": "姚华明继许桂清任营口市长（2021年许桂清辞去市长）", "overlap_org": "营口市人民政府", "overlap_period": "2021", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor", "context": "姚华明在赵长富（被查）之后长期任营口市委主要领导序列", "overlap_org": "中共营口市委", "overlap_period": "2016-2024", "confidence": "plausible"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "李进辉作为常务副市长协助市长李军主持市政府日常工作", "overlap_org": "营口市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "韩冰作为副市长受市长李军领导", "overlap_org": "营口市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "赵涵斌作为副市长兼公安局长受市长李军领导", "overlap_org": "营口市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "王正刚作为副市长受市长李军领导", "overlap_org": "营口市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "李人杰作为副市长受市长李军领导", "overlap_org": "营口市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "付波作为副市长（无党派）受市长领导", "overlap_org": "营口市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "高峰作为挂职副市长受市长李军领导", "overlap_org": "营口市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "纪委书记胡哲在市委领导下负责纪检监察", "overlap_org": "中共营口市委/营口市纪委监委", "overlap_period": "至今", "confidence": "confirmed"},
]

# ── 路径 ─────────────────────────────────────────────────────────────────

# 脚本可被多次运行，输出写入标准 data/database 与 data/graph 目录
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"


if __name__ == "__main__":
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

    import sqlite3 as _sqlite3

    conn = _sqlite3.connect(str(DB_PATH))
    try:
        count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
        print(f"      persons rows: {count}")
    finally:
        conn.close()

    print(f"\n✅ Build complete: {SLUG}")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")