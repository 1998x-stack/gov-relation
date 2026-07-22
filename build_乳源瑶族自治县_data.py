#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Ruyuan Yao Autonomous County (乳源瑶族自治县), Shaoguan, Guangdong."""

import os
import sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
sys.path.insert(0, BASE)
TMP = os.path.join(BASE, "data/tmp/guangdong_乳源瑶族自治县")
DB_PATH = os.path.join(TMP, "乳源瑶族自治县_network.db")
GEXF_PATH = os.path.join(TMP, "乳源瑶族自治县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1, "name": "黄艺坤", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-10", "birthplace": "", "education": "大学、经济学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源瑶族自治县委书记", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/content/post_2812208.html"
    },
    {
        "id": 2, "name": "唐振朝", "gender": "男", "ethnicity": "瑶族",
        "birth": "1977-05", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源瑶族自治县委副书记、县长", "current_org": "乳源瑶族自治县人民政府",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzf/content/post_2746813.html"
    },

    # ── Deputy Party Secretaries ──
    {
        "id": 3, "name": "林劲标", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-05", "birthplace": "", "education": "研究生、法律硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源瑶族自治县委副书记", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/content/post_2083360.html"
    },
    {
        "id": 4, "name": "林欣", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-10", "birthplace": "", "education": "大学、管理学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源瑶族自治县委副书记", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/content/post_2540167.html"
    },

    # ── Standing Committee Members ──
    {
        "id": 5, "name": "陈希茂", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县委常委", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/"
    },
    {
        "id": 6, "name": "李继发", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县委常委", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/"
    },
    {
        "id": 7, "name": "朱秀华", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县委常委", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/"
    },
    {
        "id": 8, "name": "叶飞", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县委常委、县政府副县长", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/"
    },
    {
        "id": 9, "name": "董新月", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县委常委", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/"
    },
    {
        "id": 10, "name": "张孝明", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县委常委", "current_org": "中共乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xw/"
    },

    # ── County Government Members ──
    {
        "id": 11, "name": "陈小可", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县副县长", "current_org": "乳源瑶族自治县人民政府",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzf/"
    },
    {
        "id": 12, "name": "杨贤冰", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "乳源县副县长", "current_org": "乳源瑶族自治县人民政府",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzf/"
    },
    {
        "id": 13, "name": "刘俊斌", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县副县长", "current_org": "乳源瑶族自治县人民政府",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzf/"
    },
    {
        "id": 14, "name": "杨川毅", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县副县长", "current_org": "乳源瑶族自治县人民政府",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzf/"
    },
    {
        "id": 15, "name": "邓晓羚", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "乳源县副县长", "current_org": "乳源瑶族自治县人民政府",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzf/"
    },
    {
        "id": 16, "name": "利绍聪", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县副县长", "current_org": "乳源瑶族自治县人民政府",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzf/"
    },

    # ── People's Congress ──
    {
        "id": 17, "name": "张军", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县人大常委会主任", "current_org": "乳源瑶族自治县人民代表大会常务委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xrd/content/post_229738.html"
    },
    {
        "id": 18, "name": "简连英", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县人大常委会副主任", "current_org": "乳源瑶族自治县人民代表大会常务委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xrd/"
    },
    {
        "id": 19, "name": "吴巧英", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "乳源县人大常委会副主任", "current_org": "乳源瑶族自治县人民代表大会常务委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xrd/"
    },
    {
        "id": 20, "name": "秦正京", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县人大常委会副主任", "current_org": "乳源瑶族自治县人民代表大会常务委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xrd/"
    },
    {
        "id": 21, "name": "吴衍雄", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县人大常委会副主任", "current_org": "乳源瑶族自治县人民代表大会常务委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xrd/"
    },
    {
        "id": 22, "name": "王东", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县人大常委会副主任", "current_org": "乳源瑶族自治县人民代表大会常务委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xrd/"
    },

    # ── CPPCC ──
    {
        "id": 23, "name": "林昌卫", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "乳源县政协主席", "current_org": "中国人民政治协商会议乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzx/content/post_229753.html"
    },
    {
        "id": 24, "name": "李智军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "乳源县政协副主席", "current_org": "中国人民政治协商会议乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzx/"
    },
    {
        "id": 25, "name": "赵天聪", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "乳源县政协副主席", "current_org": "中国人民政治协商会议乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzx/"
    },
    {
        "id": 26, "name": "李东生", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "乳源县政协副主席", "current_org": "中国人民政治协商会议乳源瑶族自治县委员会",
        "source": "https://www.ruyuan.gov.cn/zwgk/ldzc/xzx/"
    },
]

organizations = [
    {
        "id": 1, "name": "中共乳源瑶族自治县委员会", "type": "党委", "level": "县处级",
        "parent": "中共韶关市委员会", "location": "广东省韶关市乳源瑶族自治县"
    },
    {
        "id": 2, "name": "乳源瑶族自治县人民政府", "type": "政府", "level": "县处级",
        "parent": "韶关市人民政府", "location": "广东省韶关市乳源瑶族自治县"
    },
    {
        "id": 3, "name": "乳源瑶族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级",
        "parent": "韶关市人大常委会", "location": "广东省韶关市乳源瑶族自治县"
    },
    {
        "id": 4, "name": "中国人民政治协商会议乳源瑶族自治县委员会", "type": "政协", "level": "县处级",
        "parent": "韶关市政协", "location": "广东省韶关市乳源瑶族自治县"
    },
]

positions = [
    # ── Huang Yikun (黄艺坤) ──
    {"person_id": 1, "org_id": 1, "title": "乳源瑶族自治县委书记", "start": "", "end": "present",
     "rank": "县处级", "note": "主持县委全面工作。联系桂头镇。"},

    # ── Tang Zhenzhao (唐振朝) ──
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "县处级", "note": "兼任县长"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present",
     "rank": "县处级", "note": "主持县政府全面工作。负责审计工作。分管县审计局。"},

    # ── Lin Jinbiao (林劲标) ──
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "县处级", "note": "协助黄艺坤同志抓百千万工程有关重点项目建设，协调省组团纵向帮扶支持县域高质量发展工作。"},

    # ── Lin Xin (林欣) ──
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "县处级", "note": "协助黄艺坤同志抓党的建设工作。负责百千万工程、三农、乡村振兴、群团工作。联系大桥镇。"},

    # ── Standing Committee ──
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县处级", "note": ""},

    # ── County Government Deputies ──
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县处级", "note": ""},

    # ── People's Congress ──
    {"person_id": 17, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "县处级", "note": "主持县人大常委会全面工作"},
    {"person_id": 18, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},

    # ── CPPCC ──
    {"person_id": 23, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "县处级", "note": "主持县政协全面工作"},
    {"person_id": 24, "org_id": 4, "title": "县政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "县政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "县政协副主席", "start": "", "end": "present", "rank": "副县处级", "note": ""},
]

relationships = [
    # ── Leadership Core Relationships ──
    {
        "person_a": 1, "person_b": 2, "type": "superior_subordinate",
        "context": "县委书记与县长搭档", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 3, "type": "superior_subordinate",
        "context": "县委书记与副书记", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 4, "type": "superior_subordinate",
        "context": "县委书记与副书记", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    # ── Standing Committee colleagues ──
    {
        "person_a": 2, "person_b": 3, "type": "overlap",
        "context": "县委副书记同事关系", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 4, "type": "overlap",
        "context": "县委副书记同事关系", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 3, "person_b": 4, "type": "overlap",
        "context": "县委副书记同事关系", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    # ── Standing Committee to BS Committee ──
    {
        "person_a": 1, "person_b": 5, "type": "superior_subordinate",
        "context": "县委书记与县委常委", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 6, "type": "superior_subordinate",
        "context": "县委书记与县委常委", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 7, "type": "superior_subordinate",
        "context": "县委书记与县委常委", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 8, "type": "superior_subordinate",
        "context": "县委书记与县委常委、副县长", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 9, "type": "superior_subordinate",
        "context": "县委书记与县委常委", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 10, "type": "superior_subordinate",
        "context": "县委书记与县委常委", "overlap_org": "中共乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    # ── Mayor to Government Deputies ──
    {
        "person_a": 2, "person_b": 11, "type": "superior_subordinate",
        "context": "县长与副县长", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 12, "type": "superior_subordinate",
        "context": "县长与副县长", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 13, "type": "superior_subordinate",
        "context": "县长与副县长", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 14, "type": "superior_subordinate",
        "context": "县长与副县长", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 15, "type": "superior_subordinate",
        "context": "县长与副县长", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 16, "type": "superior_subordinate",
        "context": "县长与副县长", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    # ── Government deputy colleague relationship ──
    {
        "person_a": 8, "person_b": 11, "type": "overlap",
        "context": "副县长同事关系", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 8, "person_b": 12, "type": "overlap",
        "context": "副县长同事关系", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 8, "person_b": 13, "type": "overlap",
        "context": "副县长同事关系", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 8, "person_b": 14, "type": "overlap",
        "context": "副县长同事关系", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 8, "person_b": 15, "type": "overlap",
        "context": "副县长同事关系", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 8, "person_b": 16, "type": "overlap",
        "context": "副县长同事关系", "overlap_org": "乳源瑶族自治县人民政府",
        "overlap_period": "present", "confidence": "confirmed"
    },
    # ── Municipal Congress and Government ──
    {
        "person_a": 1, "person_b": 17, "type": "overlap",
        "context": "县委与人大的党政领导关系", "overlap_org": "乳源瑶族自治县",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 23, "type": "overlap",
        "context": "县委与政协的党政领导关系", "overlap_org": "乳源瑶族自治县",
        "overlap_period": "present", "confidence": "confirmed"
    },
    # ── Municipal Congress colleague ──
    {
        "person_a": 17, "person_b": 18, "type": "superior_subordinate",
        "context": "人大常委会主任与副主任", "overlap_org": "乳源瑶族自治县人民代表大会常务委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 17, "person_b": 19, "type": "superior_subordinate",
        "context": "人大常委会主任与副主任", "overlap_org": "乳源瑶族自治县人民代表大会常务委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 17, "person_b": 20, "type": "superior_subordinate",
        "context": "人大常委会主任与副主任", "overlap_org": "乳源瑶族自治县人民代表大会常务委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 17, "person_b": 21, "type": "superior_subordinate",
        "context": "人大常委会主任与副主任", "overlap_org": "乳源瑶族自治县人民代表大会常务委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 17, "person_b": 22, "type": "superior_subordinate",
        "context": "人大常委会主任与副主任", "overlap_org": "乳源瑶族自治县人民代表大会常务委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    # ── CPPCC colleague ──
    {
        "person_a": 23, "person_b": 24, "type": "superior_subordinate",
        "context": "政协主席与副主席", "overlap_org": "中国人民政治协商会议乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 23, "person_b": 25, "type": "superior_subordinate",
        "context": "政协主席与副主席", "overlap_org": "中国人民政治协商会议乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
    {
        "person_a": 23, "person_b": 26, "type": "superior_subordinate",
        "context": "政协主席与副主席", "overlap_org": "中国人民政治协商会议乳源瑶族自治县委员会",
        "overlap_period": "present", "confidence": "confirmed"
    },
]

# ── BUILD ────────────────────────────────────────────────────────────

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

run_build(
    slug="乳源瑶族自治县",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
    overwrite=True,
)

print("Build complete.")
print(f"  DB:   {DB_PATH}")
print(f"  GEXF: {GEXF_PATH}")
