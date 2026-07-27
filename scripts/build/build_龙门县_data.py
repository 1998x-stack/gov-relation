#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 龙门县 leadership network.

Data source: www.longmen.gov.cn (official government website), www.huizhou.gov.cn
Information currency: 2026-07-22 (current as of July 2026)
"""
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "龙门县"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # === 县委常委 (County Party Committee Standing Committee) ===
    {
        "id": 1, "name": "刘洪添", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年8月", "birthplace": "广东惠城", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "1987年7月",
        "current_post": "惠州市政协党组成员、副主席，龙门县委书记",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 2, "name": "王洋", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年8月", "birthplace": "", "education": "在职博士研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委副书记，县政府党组书记、县长",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 3, "name": "陈琳", "gender": "女", "ethnicity": "汉族",
        "birth": "1980年6月", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委副书记（挂职）",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 4, "name": "黄卓豪", "gender": "男", "ethnicity": "汉族",
        "birth": "1981年10月", "birthplace": "", "education": "在职农业推广硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委副书记、政法委书记",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 5, "name": "罗光少", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年9月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委、统战部部长、县政协党组副书记，三级调研员",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 6, "name": "李锋", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年9月", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委，县政府党组成员、副县长（挂职）",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 7, "name": "陈洁", "gender": "女", "ethnicity": "回族",
        "birth": "1979年5月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委、宣传部部长，三级调研员",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 8, "name": "张志文", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年3月", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委，县政府党组副书记、常务副县长",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 9, "name": "毛振辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年3月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委、组织部部长，三级调研员",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 10, "name": "陈职勇", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年10月", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委、县政府副县长",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 11, "name": "邓定文", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年5月", "birthplace": "", "education": "大专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委、县纪委书记、县监委代理主任",
        "current_org": "中共龙门县纪律检查委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 12, "name": "张锐源", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年3月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县委常委，县委办公室主任、县委改革办主任、县直机关工委书记",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    # === 县政府其他副县长 (non-standing-committee) ===
    {
        "id": 13, "name": "张振东", "gender": "男", "ethnicity": "满族",
        "birth": "1987年10月", "birthplace": "", "education": "研究生",
        "party_join": "", "work_start": "",
        "current_post": "龙门县政府党组成员、副县长",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/index.html",
    },
    {
        "id": 14, "name": "邬淑娴", "gender": "女", "ethnicity": "汉族",
        "birth": "1976年3月", "birthplace": "", "education": "在职大学",
        "party_join": "", "work_start": "",
        "current_post": "龙门县政府党组成员、副县长（挂职贵州省黔西南州普安县）",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/index.html",
    },
    {
        "id": 15, "name": "郝治翰", "gender": "男", "ethnicity": "汉族",
        "birth": "1992年5月", "birthplace": "", "education": "博士研究生",
        "party_join": "", "work_start": "",
        "current_post": "龙门县政府党组成员、副县长兼龙江镇党委书记",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/index.html",
    },
    {
        "id": 16, "name": "王庆胜", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年4月", "birthplace": "", "education": "大专",
        "party_join": "", "work_start": "",
        "current_post": "龙门县政府党组成员、副县长兼县公安局局长",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/index.html",
    },
    {
        "id": 17, "name": "刘业丰", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年10月", "birthplace": "", "education": "在职大学",
        "party_join": "", "work_start": "",
        "current_post": "龙门县政府党组成员、副县长",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/index.html",
    },
    {
        "id": 18, "name": "陈达婷", "gender": "女", "ethnicity": "汉族",
        "birth": "1984年8月", "birthplace": "", "education": "在职研究生",
        "party_join": "", "work_start": "",
        "current_post": "龙门县政府党组成员、副县长",
        "current_org": "龙门县人民政府",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrmzf/index.html",
    },
    # === 人大 (People's Congress) ===
    {
        "id": 19, "name": "古慧平", "gender": "男", "ethnicity": "汉族",
        "birth": "1966年8月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县人大常委会主任",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    {
        "id": 20, "name": "刘远彬", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年9月", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县人大常委会党组书记、主任人选",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    {
        "id": 21, "name": "王卫良", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年4月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县人大常委会党组成员、副主任，二级调研员",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    {
        "id": 22, "name": "林建辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年3月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县人大常委会党组成员、副主任，三级调研员",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    {
        "id": 23, "name": "蓝月清", "gender": "女", "ethnicity": "汉族",
        "birth": "1968年3月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县人大常委会党组成员、副主任，三级调研员",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    {
        "id": 24, "name": "张年胜", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年8月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县人大常委会党组成员、副主任，县总工会党组书记、主席，三级调研员",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    {
        "id": 25, "name": "李穗华", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年3月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县人大常委会党组成员、副主任",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    {
        "id": 26, "name": "刘婷英", "gender": "女", "ethnicity": "汉族",
        "birth": "1973年9月", "birthplace": "", "education": "在职大学",
        "party_join": "民革党员", "work_start": "",
        "current_post": "龙门县人大常委会副主任人选",
        "current_org": "龙门县人大常委会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/lmxrdcwh/index.html",
    },
    # === 政协 (CPPCC) ===
    {
        "id": 27, "name": "林大升", "gender": "男", "ethnicity": "汉族",
        "birth": "1969年9月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县政协党组书记、主席",
        "current_org": "政协龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/index.html",
    },
    {
        "id": 28, "name": "王宇文", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年5月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县政协党组成员、副主席，三级调研员",
        "current_org": "政协龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/index.html",
    },
    {
        "id": 29, "name": "梁志斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年7月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县政协党组成员、副主席，三级调研员",
        "current_org": "政协龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/index.html",
    },
    {
        "id": 30, "name": "黄育贤", "gender": "男", "ethnicity": "汉族",
        "birth": "1969年1月", "birthplace": "", "education": "大专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县政协党组成员、副主席，三级调研员",
        "current_org": "政协龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/index.html",
    },
    {
        "id": 31, "name": "罗天威", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年9月", "birthplace": "", "education": "大学",
        "party_join": "民盟盟员", "work_start": "",
        "current_post": "龙门县政协副主席",
        "current_org": "政协龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zxlmxwyh/index.html",
    },
    # === 纪委 (Discipline Inspection Commission) ===
    {
        "id": 32, "name": "赖亮珊", "gender": "女", "ethnicity": "汉族",
        "birth": "1981年12月", "birthplace": "", "education": "大学/法学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县纪委副书记、县监委副主任，四级调研员、四级高级监察官",
        "current_org": "中共龙门县纪律检查委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxjljcwyh/index.html",
    },
    {
        "id": 33, "name": "黄育金", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年6月", "birthplace": "", "education": "大学/历史学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "龙门县纪委副书记、县监委副主任，一级监察官",
        "current_org": "中共龙门县纪律检查委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxjljcwyh/index.html",
    },
    # === 前任领导 (Predecessors) ===
    {
        "id": 34, "name": "陈伟良", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记（约2018-2021）",
        "current_org": "中共龙门县委员会",
        "source": "http://www.longmen.gov.cn/lmxrmzfmhwz/zwgk/zzjg/ldzc/zglmxw/index.html",
    },
    {
        "id": 35, "name": "段致辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年4月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "惠州市人民政府党组成员、副市长（前任龙门县长）",
        "current_org": "惠州市人民政府",
        "source": "http://www.huizhou.gov.cn/zwgk/ldzc/hzsrmzf/fsz/content/post_4583067.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共龙门县委员会", "type": "党委", "level": "县", "parent": "中共惠州市委", "location": "广东省惠州市龙门县"},
    {"id": 2, "name": "龙门县人民政府", "type": "政府", "level": "县", "parent": "惠州市人民政府", "location": "广东省惠州市龙门县"},
    {"id": 3, "name": "龙门县人大常委会", "type": "人大", "level": "县", "parent": "惠州市人大常委会", "location": "广东省惠州市龙门县"},
    {"id": 4, "name": "政协龙门县委员会", "type": "政协", "level": "县", "parent": "政协惠州市委员会", "location": "广东省惠州市龙门县"},
    {"id": 5, "name": "中共龙门县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共惠州市纪委", "location": "广东省惠州市龙门县"},
    {"id": 6, "name": "惠州市政协", "type": "政协", "level": "地级市", "parent": "广东省政协", "location": "广东省惠州市"},
    {"id": 7, "name": "惠州市人民政府", "type": "政府", "level": "地级市", "parent": "广东省人民政府", "location": "广东省惠州市"},
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 刘洪添
    {"person_id": 1, "org_id": 1, "title": "龙门县委书记（兼惠州市政协副主席）", "start_date": "2022-09", "end_date": "", "rank": "副厅级", "note": "2025年2月起兼任惠州市政协副主席"},
    {"person_id": 1, "org_id": 6, "title": "惠州市政协党组成员、副主席", "start_date": "2025-02", "end_date": "", "rank": "副厅级", "note": "高配"},
    # 王洋
    {"person_id": 2, "org_id": 2, "title": "龙门县县长", "start_date": "2025-04", "end_date": "", "rank": "正处级", "note": "2025年4月10日当选"},
    {"person_id": 2, "org_id": 1, "title": "龙门县委副书记", "start_date": "~2025", "end_date": "", "rank": "副处级", "note": ""},
    # 其他县委常委
    {"person_id": 3, "org_id": 1, "title": "龙门县委副书记（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "东西部协作"},
    {"person_id": 4, "org_id": 1, "title": "龙门县委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "龙门县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 6, "org_id": 2, "title": "龙门县委常委、副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "龙门县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "回族，三级调研员"},
    {"person_id": 8, "org_id": 2, "title": "龙门县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "龙门县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 10, "org_id": 2, "title": "龙门县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "龙门县委常委、县纪委书记、县监委代理主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "2026年7月任命为监委代理主任"},
    {"person_id": 12, "org_id": 1, "title": "龙门县委常委、县委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副县长（非常委）
    {"person_id": 13, "org_id": 2, "title": "龙门县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "满族"},
    {"person_id": 14, "org_id": 2, "title": "龙门县副县长（挂职贵州）", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职贵州省黔西南州普安县"},
    {"person_id": 15, "org_id": 2, "title": "龙门县副县长兼龙江镇党委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "1992年生，博士"},
    {"person_id": 16, "org_id": 2, "title": "龙门县副县长兼县公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "龙门县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "龙门县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "女"},
    # 人大
    {"person_id": 19, "org_id": 3, "title": "龙门县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "龙门县人大常委会党组书记、主任人选", "start_date": "", "end_date": "", "rank": "正处级", "note": "换届过渡期"},
    {"person_id": 21, "org_id": 3, "title": "龙门县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "二级调研员"},
    {"person_id": 22, "org_id": 3, "title": "龙门县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 23, "org_id": 3, "title": "龙门县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "女，三级调研员"},
    {"person_id": 24, "org_id": 3, "title": "龙门县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼县总工会主席"},
    {"person_id": 25, "org_id": 3, "title": "龙门县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 3, "title": "龙门县人大常委会副主任人选", "start_date": "", "end_date": "", "rank": "副处级", "note": "民革党员"},
    # 政协
    {"person_id": 27, "org_id": 4, "title": "龙门县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 28, "org_id": 4, "title": "龙门县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 29, "org_id": 4, "title": "龙门县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 30, "org_id": 4, "title": "龙门县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 31, "org_id": 4, "title": "龙门县政协副主席", "start_date": "2025-02", "end_date": "", "rank": "副处级", "note": "民盟盟员"},
    # 纪委副书记
    {"person_id": 32, "org_id": 5, "title": "龙门县纪委副书记、县监委副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "女"},
    {"person_id": 33, "org_id": 5, "title": "龙门县纪委副书记、县监委副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 前任
    {"person_id": 34, "org_id": 1, "title": "龙门县委书记", "start_date": "~2018", "end_date": "~2021", "rank": "正处级", "note": "刘洪添的前任"},
    {"person_id": 35, "org_id": 2, "title": "龙门县县长（前任）", "start_date": "~2019", "end_date": "~2024", "rank": "正处级", "note": "后升任惠州市副市长"},
    {"person_id": 35, "org_id": 7, "title": "惠州市副市长", "start_date": "~2024", "end_date": "", "rank": "副厅级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    # 县委书记—县长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记—县长", "overlap_org": "龙门县四套班子", "overlap_period": "2025—"},
    # 县委常委会
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记—副书记（挂职）", "overlap_org": "中共龙门县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记—副书记/政法委书记", "overlap_org": "中共龙门县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记—统战部长", "overlap_org": "中共龙门县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "书记—宣传部长", "overlap_org": "中共龙门县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "书记—组织部长", "overlap_org": "中共龙门县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "书记—纪委书记", "overlap_org": "中共龙门县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "书记—县委办主任", "overlap_org": "中共龙门县委", "overlap_period": ""},
    # 县长—副县长（政府班子）
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长（挂职）", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长—副县长", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "县长—副县长", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "县长—副县长兼公安局长", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "县长—副县长", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "县长—副县长", "overlap_org": "龙门县人民政府", "overlap_period": ""},
    # 前任—现任书记
    {"person_a": 34, "person_b": 1, "type": "前后任", "context": "前任县委书记→现任县委书记", "overlap_org": "中共龙门县委", "overlap_period": "~2021交接"},
    # 前任—现任县长（段致辉是前任，王洋是现任 — 中间可能有陈宇浩过渡）
    {"person_a": 35, "person_b": 2, "type": "前后任", "context": "前任县长→现任县长", "overlap_org": "龙门县人民政府", "overlap_period": "~2024-2025交接"},
    # 人大—县委
    {"person_a": 19, "person_b": 1, "type": "列席监督", "context": "人大常委会主任—县委书记", "overlap_org": "龙门县四套班子", "overlap_period": ""},
    # 政协—县委
    {"person_a": 27, "person_b": 1, "type": "列席监督", "context": "政协主席—县委书记", "overlap_org": "龙门县四套班子", "overlap_period": ""},
    # 前任县长—去向（段致辉升任惠州市副市长）
    {"person_a": 35, "person_b": 1, "type": "前后任", "context": "前任县长→现任县委书记（曾为党政搭档）", "overlap_org": "龙门县四套班子", "overlap_period": "2021-2024"},
]

# ── Run Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "龙门县_network.db",
        gexf_path=GRAPH_DIR / "龙门县_network.gexf",
        overwrite=True,
    )
    print("Done: 龙门县 network built.")
