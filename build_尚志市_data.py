#!/usr/bin/env python3
"""Build script for 尚志市 (Shangzhi City) leadership network data.

尚志市 is a county-level city under 哈尔滨市, 黑龙江省.
Data sourced from shangzhi.gov.cn official leadership pages (as of 2026-07).
"""

from pathlib import Path
import sys

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Persons ──────────────────────────────────────────────────────────────────
# ID range: 1-20 for persons, 21-30 for organizations

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "于彦波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "黑龙江讷河",
        "education": "哈尔滨工业大学控制科学与工程专业研究生，工学博士",
        "party_join": "1999-06",
        "work_start": "2004-08",
        "current_post": "尚志市委书记",
        "current_org": "中共尚志市委员会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/yuyb/202501/c01_1035774.shtml",
    },
    {
        "id": 2,
        "name": "杜召恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-02",
        "birthplace": "黑龙江宾县",
        "education": "中共黑龙江省委党校经济管理专业毕业，硕士",
        "party_join": "1998-06",
        "work_start": "1998-07",
        "current_post": "尚志市委副书记、代市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/duzh/202505/c01_1060899.shtml",
    },
    # ──市委领导──
    {
        "id": 3,
        "name": "王超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-03",
        "birthplace": "黑龙江依兰",
        "education": "黑龙江八一农垦大学经济贸易学院会计专业毕业，研究生",
        "party_join": "1997-05",
        "work_start": "1998-07",
        "current_post": "尚志市委副书记",
        "current_org": "中共尚志市委员会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/wchao/202412/c01_1030675.shtml",
    },
    {
        "id": 4,
        "name": "李海东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-02",
        "birthplace": "黑龙江巴彦",
        "education": "研究生",
        "party_join": "2008-11",
        "work_start": "2013-11",
        "current_post": "尚志市委常委、组织部部长",
        "current_org": "中共尚志市委员会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100145/202301/c01_234568.shtml",
    },
    {
        "id": 5,
        "name": "王海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "黑龙江巴彦",
        "education": "大学",
        "party_join": "2002-12",
        "work_start": "2003-07",
        "current_post": "尚志市委常委、纪委书记、监委主任",
        "current_org": "中共尚志市纪律检查委员会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/wht/202507/c01_1068874.shtml",
    },
    {
        "id": 6,
        "name": "钟声",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1979-04",
        "birthplace": "黑龙江双城",
        "education": "大连陆军学院毕业，大学",
        "party_join": "2000",
        "work_start": "2002",
        "current_post": "尚志市委常委、人民武装部上校部长",
        "current_org": "尚志市人民武装部",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/zhongs/202412/c01_1030917.shtml",
    },
    {
        "id": 7,
        "name": "彭森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "河南固始",
        "education": "华中科技大学新闻学专业毕业，研究生",
        "party_join": "1999-12",
        "work_start": "2001-07",
        "current_post": "尚志市委常委、政府副市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/psen/202412/c01_1031594.shtml",
    },
    {
        "id": 8,
        "name": "李毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市委常委",
        "current_org": "中共尚志市委员会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/liyi1/202505/c01_1060261.shtml",
    },
    {
        "id": 9,
        "name": "赵莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市委常委",
        "current_org": "中共尚志市委员会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/zhaoying/202507/c01_1070302.shtml",
    },
    {
        "id": 10,
        "name": "刘景峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "黑龙江依兰",
        "education": "中共黑龙江省委党校中文专业毕业，大学",
        "party_join": "2003-06",
        "work_start": "1998-07",
        "current_post": "尚志市委常委、市政府副市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/ljf/202301/c01_1111815.shtml",
    },
    {
        "id": 11,
        "name": "祖立巍",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市委常委",
        "current_org": "中共尚志市委员会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/zlwq/202404/c01_1132561.shtml",
    },
    # ──市政府副市长──
    {
        "id": 12,
        "name": "刘凤君",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市副市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100161/202301/c01_234583.shtml",
    },
    {
        "id": 13,
        "name": "张君",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市副市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/zhangj/202507/c01_1070301.shtml",
    },
    {
        "id": 14,
        "name": "宫艳彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市副市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/gyb/202512/c01_1098134.shtml",
    },
    {
        "id": 15,
        "name": "韩玉璞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市副市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/hyp/202604/c01_1121771.shtml",
    },
    {
        "id": 16,
        "name": "於德华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市副市长",
        "current_org": "尚志市人民政府",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100160/202301/c01_234581.shtml",
    },
    # ──市人大领导──
    {
        "id": 17,
        "name": "聂俊清",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市人大常委会主任",
        "current_org": "尚志市人大常委会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100147/202301/c01_218928.shtml",
    },
    {
        "id": 18,
        "name": "呼大鹏",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1968-11",
        "birthplace": "辽宁开原",
        "education": "黑龙江大学历史专业毕业，大学",
        "party_join": "1996-05",
        "work_start": "1991-09",
        "current_post": "尚志市人大常委会党组副书记、副主任",
        "current_org": "尚志市人大常委会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100148/202301/c01_234573.shtml",
    },
    {
        "id": 19,
        "name": "张晓程",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市人大常委会副主任",
        "current_org": "尚志市人大常委会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/zxc/202503/c01_1052370.shtml",
    },
    {
        "id": 20,
        "name": "王伟玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市人大常委会副主任",
        "current_org": "尚志市人大常委会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100149/202301/c01_234575.shtml",
    },
    {
        "id": 21,
        "name": "台木礼",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市人大常委会副主任",
        "current_org": "尚志市人大常委会",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100151/202301/c01_234576.shtml",
    },
    # ──市政协领导──
    {
        "id": 22,
        "name": "张兴国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市政协主席",
        "current_org": "尚志市政协",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100164/202301/c01_234587.shtml",
    },
    {
        "id": 23,
        "name": "郭文锐",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市政协副主席",
        "current_org": "尚志市政协",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100167/202301/c01_234589.shtml",
    },
    {
        "id": 24,
        "name": "蒋兵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "尚志市政协副主席",
        "current_org": "尚志市政协",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c100166/202301/c01_234590.shtml",
    },
    # ──前任领导──
    {
        "id": 25,
        "name": "张超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c110033/202402/c01_969294.shtml",
    },
    {
        "id": 26,
        "name": "孙德志",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.shangzhi.gov.cn/szsrmzf/c110033/201901/c01_224531.shtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共尚志市委员会", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委员会", "location": "尚志市"},
    {"id": 2, "name": "尚志市人民政府", "type": "政府", "level": "县级", "parent": "哈尔滨市人民政府", "location": "尚志市"},
    {"id": 3, "name": "中共尚志市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共哈尔滨市纪律检查委员会", "location": "尚志市"},
    {"id": 4, "name": "尚志市人民武装部", "type": "事业单位", "level": "县级", "parent": "哈尔滨警备区", "location": "尚志市"},
    {"id": 5, "name": "尚志市人大常委会", "type": "人大", "level": "县级", "parent": "哈尔滨市人大常委会", "location": "尚志市"},
    {"id": 6, "name": "尚志市政协", "type": "政协", "level": "县级", "parent": "哈尔滨市政协", "location": "尚志市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 于彦波
    {"person_id": 1, "org_id": 1, "title": "尚志市委书记", "start_date": "2026", "end_date": "present",
     "rank": "正处级", "note": "前身为尚志市长，2026年7月辞去市长职务转任市委书记"},
    {"person_id": 1, "org_id": 2, "title": "尚志市市长", "start_date": "", "end_date": "2026-07",
     "rank": "正处级", "note": "2026年7月15日第九届人大常委会第四十四次会议接受辞去市长职务"},
    # 杜召恒
    {"person_id": 2, "org_id": 2, "title": "尚志市委副书记、代市长", "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "2026年7月被任命为代市长"},
    # 王超
    {"person_id": 3, "org_id": 1, "title": "尚志市委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 李海东
    {"person_id": 4, "org_id": 1, "title": "尚志市委常委、组织部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 王海涛
    {"person_id": 5, "org_id": 3, "title": "尚志市委常委、纪委书记、监委主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 钟声
    {"person_id": 6, "org_id": 4, "title": "尚志市委常委、人民武装部上校部长", "start_date": "", "end_date": "present",
     "rank": "上校", "note": ""},
    # 彭森
    {"person_id": 7, "org_id": 2, "title": "尚志市委常委、政府副市长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 李毅
    {"person_id": 8, "org_id": 1, "title": "尚志市委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 赵莹
    {"person_id": 9, "org_id": 1, "title": "尚志市委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 刘景峰
    {"person_id": 10, "org_id": 2, "title": "尚志市委常委、市政府副市长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责工业、发改、统计、产业、招商引资"},
    # 祖立巍
    {"person_id": 11, "org_id": 1, "title": "尚志市委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    # 市政府副市长
    {"person_id": 12, "org_id": 2, "title": "尚志市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "尚志市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "尚志市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "尚志市副市长", "start_date": "2026-04", "end_date": "present", "rank": "副处级", "note": "2026年4月28日被任命"},
    {"person_id": 16, "org_id": 2, "title": "尚志市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 市人大
    {"person_id": 17, "org_id": 5, "title": "尚志市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 5, "title": "尚志市人大常委会党组副书记、副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 5, "title": "尚志市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 5, "title": "尚志市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 5, "title": "尚志市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 市政协
    {"person_id": 22, "org_id": 6, "title": "尚志市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 6, "title": "尚志市政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 6, "title": "尚志市政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 前任 - 张超
    {"person_id": 25, "org_id": 2, "title": "尚志市市长", "start_date": "2021", "end_date": "2025",
     "rank": "正处级", "note": "写了2021-2023年政府工作报告"},
    # 前任 - 孙德志
    {"person_id": 26, "org_id": 2, "title": "尚志市市长", "start_date": "2016", "end_date": "2020",
     "rank": "正处级", "note": "写了2016-2018年政府工作报告"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 于彦波 ↔ 杜召恒 (书记-代市长搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与代市长工作搭档", "overlap_org": "中共尚志市委员会/尚志市人民政府",
     "overlap_period": "2026-07至今"},
    # 于彦波 ↔ 王超 (书记-副书记)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与副书记工作关系", "overlap_org": "中共尚志市委员会",
     "overlap_period": "2026年至今"},
    # 杜召恒 ↔ 刘景峰 (代市长-副市长)
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "代市长与常务副市长关系", "overlap_org": "尚志市人民政府",
     "overlap_period": "2026-07至今"},
    # 于彦波 ↔ 刘景峰 (书记-副市长/常委)
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "市委常委会共事", "overlap_org": "中共尚志市委员会",
     "overlap_period": "2026年至今"},
    # 王海涛 ↔ 韩玉璞 (纪委-副市长，一起督导检查)
    {"person_a": 5, "person_b": 15, "type": "overlap",
     "context": "共同督导检查黑龙宫镇防汛及安全生产工作",
     "overlap_org": "尚志市", "overlap_period": "2026-06"},
    # 彭森 ↔ 刘景峰 (协助招商引资)
    {"person_a": 7, "person_b": 10, "type": "overlap",
     "context": "彭森协助刘景峰抓招商引资工作", "overlap_org": "尚志市人民政府",
     "overlap_period": ""},
    # 前任-现任关系
    {"person_a": 1, "person_b": 25, "type": "predecessor_successor",
     "context": "于彦波接替张超担任尚志市长（于原为市长后任书记）",
     "overlap_org": "尚志市人民政府", "overlap_period": "2021-2026"},
    {"person_a": 25, "person_b": 26, "type": "predecessor_successor",
     "context": "张超接替孙德志担任尚志市长", "overlap_org": "尚志市人民政府",
     "overlap_period": "2016-2021"},
    # 故乡关联 - 于彦波(讷河人)与杜召恒(宾县人)无直接故乡关联
    # 王超(依兰人)与刘景峰(依兰人) - 同乡
    {"person_a": 3, "person_b": 10, "type": "same_native_place",
     "context": "同为黑龙江依兰人", "overlap_org": "",
     "overlap_period": ""},
]

# ── Build ────────────────────────────────────────────────────────────────────

SLUG = "尚志市"
# When run from staging dir, write there; when run from repo root, write to canonical dirs
SCRIPT_DIR = Path(__file__).resolve().parent
if SCRIPT_DIR.name.startswith("heilongjiang") or "tmp" in str(SCRIPT_DIR):
    # Staging mode
    DB_PATH = SCRIPT_DIR / "尚志市_network.db"
    GEXF_PATH = SCRIPT_DIR / "尚志市_network.gexf"
else:
    # Canonical mode
    DB_PATH = DATABASE_DIR / "尚志市_network.db"
    GEXF_PATH = GRAPH_DIR / "尚志市_network.gexf"

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
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

    # Verify
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    for table in ("persons", "organizations", "positions", "relationships"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    print(f"Done: {DB_PATH}")
    print(f"Done: {GEXF_PATH}")
