#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 米脂县, 榆林市, 陕西省."""

import os
import sys
from datetime import date
from pathlib import Path

# Add project root to path so gov_relation module is importable
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths (staging) ────────────────────────────────────────────────────
TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / "米脂县_network.db"
GEXF_PATH = TMP_DIR / "米脂县_network.gexf"

# ── DATA ───────────────────────────────────────────────────────────────

TODAY = date.today().strftime("%Y-%m-%d")

persons = [
    # ── Current Top Leaders ──
    # 县委书记 王曼华 (confirmed from mizhi.gov.cn news, Baidu Baike county entry)
    {"id": 1, "name": "王曼华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委书记", "current_org": "中共米脂县委员会",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202607/t20260710_2113369.html"},

    # 县长 杨树森 (confirmed from mizhi.gov.cn official leadership page)
    {"id": 2, "name": "杨树森", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委副书记、县长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # ── 县委常委会成员 ──
    # 县委副书记 刘斌 (confirmed from 县工会十三大 article)
    {"id": 3, "name": "刘斌", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委副书记", "current_org": "中共米脂县委员会",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202601/t20260130_2071993.html"},

    # 县委常委、常务副县长 吕明韬 (confirmed from 防汛 article + 环境卫生 article)
    {"id": 4, "name": "吕明韬", "gender": "男", "ethnicity": "",
     "birth": "1982-02", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委常委、常务副县长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 县委常委、宣传部部长 高峰 (confirmed from basketball tournament article)
    {"id": 5, "name": "高峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委常委、宣传部部长", "current_org": "中共米脂县委宣传部",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202607/t20260721_2115939.html"},

    # 县委常委、县纪委书记、县监委主任 贾树林 (confirmed from 警示教育会议 article)
    {"id": 6, "name": "贾树林", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委常委、县纪委书记、县监委主任", "current_org": "中共米脂县纪律检查委员会",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202506/t20250611_2007310.html"},

    # 县委常委、组织部部长 郭波 (confirmed from 县工会十三大 article — 县委常委、组织部部长)
    {"id": 7, "name": "郭波", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委常委、组织部部长", "current_org": "中共米脂县委组织部",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202601/t20260130_2071993.html"},

    # 县委常委、副县长 叶凡 (confirmed from government leadership page)
    {"id": 8, "name": "叶凡", "gender": "男", "ethnicity": "",
     "birth": "1985-04", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委常委、副县长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 县委常委、副县长（挂职）薛斌 (confirmed from government leadership page)
    {"id": 9, "name": "薛斌", "gender": "男", "ethnicity": "",
     "birth": "1972-09", "birthplace": "", "education": "研究生，硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委常委、副县长（挂职）", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 县委常委 王刚 (confirmed from 人代会 listing — role推测为政法委书记或人武部部长)
    {"id": 10, "name": "王刚", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县委常委（具体职务待确认）", "current_org": "中共米脂县委员会",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202603/t20260311_2080241.html"},

    # ── 县政府领导班子（非常委）──
    # 副县长 郭锦伟 (confirmed from multiple news articles)
    {"id": 11, "name": "郭锦伟", "gender": "男", "ethnicity": "",
     "birth": "1973-09", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县副县长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 副县长 高鹏 (confirmed from news articles)
    {"id": 12, "name": "高鹏", "gender": "男", "ethnicity": "",
     "birth": "1987-10", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县副县长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 副县长 常志雄
    {"id": 13, "name": "常志雄", "gender": "男", "ethnicity": "",
     "birth": "1979-01", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县副县长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 副县长、县公安局局长 郝海洲
    {"id": 14, "name": "郝海洲", "gender": "男", "ethnicity": "",
     "birth": "1972-07", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县副县长、县公安局局长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 副县长 鲍雪娇
    {"id": 15, "name": "鲍雪娇", "gender": "女", "ethnicity": "",
     "birth": "1991-07", "birthplace": "", "education": "全日制硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县副县长", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 副县长（挂职）白鹏
    {"id": 16, "name": "白鹏", "gender": "男", "ethnicity": "",
     "birth": "1979-08", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县副县长（挂职）", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 县政府党组成员 姬强
    {"id": 17, "name": "姬强", "gender": "男", "ethnicity": "",
     "birth": "1983-03", "birthplace": "", "education": "工程硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县政府党组成员", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # 县政府党组成员 胡广隆
    {"id": 18, "name": "胡广隆", "gender": "男", "ethnicity": "",
     "birth": "1985-11", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县政府党组成员", "current_org": "米脂县人民政府",
     "source": "https://www.mizhi.gov.cn/zwgk/fdzdgknr/zfld/"},

    # ── 人大、政协主要领导 ──
    # 县人大常委会主任 孙文强
    {"id": 19, "name": "孙文强", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县人大常委会主任", "current_org": "米脂县人大常委会",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202607/t20260721_2115939.html"},

    # 县政协主席 胡锦涛
    {"id": 20, "name": "胡锦涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "米脂县政协主席", "current_org": "米脂县政协",
     "source": "https://www.mizhi.gov.cn/xwzx/mzyw/202607/t20260721_2115939.html"},
]

organizations = [
    {"id": 1, "name": "中共米脂县委员会", "type": "党委", "level": "县处级",
     "parent": "中共榆林市委员会", "location": "陕西省榆林市米脂县"},
    {"id": 2, "name": "米脂县人民政府", "type": "政府", "level": "县处级",
     "parent": "榆林市人民政府", "location": "陕西省榆林市米脂县"},
    {"id": 3, "name": "中共米脂县委宣传部", "type": "党委", "level": "正科级",
     "parent": "中共米脂县委员会", "location": "陕西省榆林市米脂县"},
    {"id": 4, "name": "中共米脂县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共米脂县委员会", "location": "陕西省榆林市米脂县"},
    {"id": 5, "name": "中共米脂县委组织部", "type": "党委", "level": "正科级",
     "parent": "中共米脂县委员会", "location": "陕西省榆林市米脂县"},
    {"id": 6, "name": "米脂县公安局", "type": "政府", "level": "正科级",
     "parent": "米脂县人民政府", "location": "陕西省榆林市米脂县"},
    {"id": 7, "name": "米脂县人大常委会", "type": "人大", "level": "县处级",
     "parent": "米脂县", "location": "陕西省榆林市米脂县"},
    {"id": 8, "name": "米脂县政协", "type": "政协", "level": "县处级",
     "parent": "米脂县", "location": "陕西省榆林市米脂县"},
]

positions = [
    # 王曼华
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "已确认在任，最早可追溯至2021年10月"},

    # 杨树森
    {"person_id": 2, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "兼任县长"},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "领导县政府全面工作"},

    # 刘斌
    {"person_id": 3, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "专职副书记"},

    # 吕明韬
    {"person_id": 4, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管政府常务工作"},

    # 高峰
    {"person_id": 5, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 3, "title": "宣传部部长",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": ""},

    # 贾树林
    {"person_id": 6, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 6, "org_id": 4, "title": "县纪委书记、县监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 郭波
    {"person_id": 7, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 5, "title": "组织部部长",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": "也在县政府任副县长（兼职）"},

    # 叶凡
    {"person_id": 8, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},

    # 薛斌
    {"person_id": 9, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "挂职"},
    {"person_id": 9, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "高邮-米脂对口协作"},

    # 王刚
    {"person_id": 10, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "具体职务待确认（推测为政法委书记或人武部部长）"},

    # 郭锦伟
    {"person_id": 11, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管自然资源、住建等"},

    # 高鹏
    {"person_id": 12, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管教体、文旅、市场监管等"},

    # 常志雄
    {"person_id": 13, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管民政、农业农村、水利等"},

    # 郝海洲
    {"person_id": 14, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 14, "org_id": 6, "title": "县公安局局长",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": ""},

    # 鲍雪娇
    {"person_id": 15, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管卫健、医保"},

    # 白鹏
    {"person_id": 16, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "国家能源集团定点帮扶"},

    # 姬强
    {"person_id": 17, "org_id": 2, "title": "县政府党组成员",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "国家电网驻村帮扶"},

    # 胡广隆
    {"person_id": 18, "org_id": 2, "title": "县政府党组成员",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "协助金融工作"},

    # 孙文强
    {"person_id": 19, "org_id": 7, "title": "县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},

    # 胡锦涛
    {"person_id": 20, "org_id": 8, "title": "县政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "同名，非前国家主席"},
]

relationships = [
    # 书记-县长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政正职搭档", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2021-2026"},

    # 书记-副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与专职副书记搭档", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},

    # 书记-各常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与常务副县长工作关系", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与宣传部部长工作关系", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与纪委书记工作关系", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与组织部部长工作关系", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与常委副县长工作关系", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与常委工作关系", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},

    # 县长-副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长工作关系", "overlap_org": "米脂县人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "米脂县人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "米脂县人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "米脂县人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "米脂县人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长兼公安局长工作关系", "overlap_org": "米脂县人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长工作关系", "overlap_org": "米脂县人民政府",
     "overlap_period": "2026"},

    # 副书记-各常委
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "县委副书记与宣传部部长同届中共米脂县委常委会", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "县委副书记与纪委书记同为县委常委会成员", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "县委副书记与组织部部长同为县委常委会成员", "overlap_org": "中共米脂县委员会",
     "overlap_period": "2026"},

    # 人大-政协
    {"person_a": 19, "person_b": 20, "type": "overlap",
     "context": "人大主任与政协主席同届工作关系", "overlap_org": "米脂县",
     "overlap_period": "2026"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="米脂县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")
