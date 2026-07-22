#!/usr/bin/env python3
"""Build Huogiu County (霍邱县) leadership network database and GEXF graph.

Targets: 县委书记高宗保, 县长沈勇
Research date: 2026-07-15
Sources:
  - www.huoqiu.gov.cn (official county government website)
  - 霍政秘〔2026〕39号: Government leadership division notice (2026-06-11)
  - hqrd.gov.cn: County People's Congress documents
  - Baidu Baike: 高宗保, 霍绍斌, 韦能武, 曹良喜 profiles
  - 中安在线: Shen Yong election report (2026-01-14)
  - 六安市委组织部: 任前公示 (2026-04-23)

Confidence: Current roles confirmed from official government website and documents.
  Biographical details for 高宗保 and 霍绍斌 sourced from Baidu Baike.
  Career timelines for deputy figures are partial where noted.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "霍邱县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "霍邱县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # === 1. Party Secretary (县委书记) ===
    {
        "id": 1,
        "name": "高宗保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-09",
        "birthplace": "安徽六安",
        "native_place": "安徽六安",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共霍邱县委员会",
        "source": "https://baike.baidu.com/item/%E9%AB%98%E5%AE%97%E4%BF%9D/19741409 (百度百科); https://www.huoqiu.gov.cn/zwzx/yw/38816114.html (2026-07-01 庆祝建党105周年表彰大会); https://www.huoqiu.gov.cn/zwzx/yw/38789149.html (2026-05-27 人武部党委第一书记任职)",
        "notes": "高宗保，男，汉族，1976年9月生，安徽六安人，中共党员，中央党校大学学历。2022年11月至2026年4月任六安市委农办主任，市农业农村局党组书记、局长。2026年4月23日拟任县（区）党委正职（任前公示）。2026年5月任霍邱县委书记，2026年5月27日兼任县人武部党委第一书记。主持县委全面工作。",
        "confidence": "confirmed"
    },
    # === 2. County Magistrate (县长) ===
    {
        "id": 2,
        "name": "沈勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号 2026-06-11 县政府分工通知); https://www.huoqiu.gov.cn/zwzx/yw/38816114.html (2026-07-01 庆祝建党105周年表彰大会); http://www.hqrd.gov.cn/DocHtml/1/25/12/00003184.html (韦能武辞职公告, 沈勇代理县长)",
        "notes": "沈勇，男，中共党员，现任霍邱县委副书记、县长。2025年12月22日被任命为霍邱县人民政府代理县长（接替韦能武辞职），2026年1月14日正式当选霍邱县县长。领导县政府全面工作，负责审计工作，分管审计局。",
        "confidence": "confirmed"
    },
    # === 3. Deputy Party Secretary (县委副书记) ===
    {
        "id": 3,
        "name": "朱成亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共霍邱县委员会",
        "source": "https://www.huoqiu.gov.cn/zwzx/yw/38816114.html (2026-07-01 庆祝建党105周年表彰大会, 宣读县委表彰决定); https://www.huoqiu.gov.cn/zwzx/yw/38813556.html (2026-06-28 县委理论学习中心组学习会)",
        "notes": "朱成亮，现任霍邱县委副书记。分管党务、群团、农业农村、乡村振兴等工作。2026年7月1日在庆祝建党105周年表彰大会上宣读县委表彰决定。",
        "confidence": "confirmed"
    },
    # === 4. Executive Deputy Magistrate (常务副县长) ===
    {
        "id": 4,
        "name": "王竹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号 县政府班子成员分工通知, 负责常务工作)",
        "notes": "王竹，现任霍邱县委常委、常务副县长。负责县政府常务工作，分管发改、财政、应急管理、统计、金融、税务、营商环境等。统筹协调经济开发区（合霍现代产业园）工作。",
        "confidence": "confirmed"
    },
    # === 5. Political and Legal Affairs Secretary (政法委书记) ===
    {
        "id": 5,
        "name": "周尚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共霍邱县委政法委员会",
        "source": "https://www.huoqiu.gov.cn/zwzx/yw/38814737.html (2026-07-01 县委政法委员会全体会议)",
        "notes": "周尚，现任霍邱县委常委、政法委书记。主持县委政法委工作。",
        "confidence": "confirmed"
    },
    # === 6. Propaganda Department Head (宣传部部长) ===
    {
        "id": 6,
        "name": "任长虹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共霍邱县委宣传部",
        "source": "https://www.huoqiu.gov.cn/zwzx/yw/38807397.html (2026-06-11 县文学艺术中心揭牌)",
        "notes": "任长虹，现任霍邱县委常委、宣传部部长。主持县委宣传部工作。",
        "confidence": "confirmed"
    },
    # === 7. County Party Standing Committee / Deputy Magistrate (县委常委、副县长) ===
    {
        "id": 7,
        "name": "毛玲霞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号); https://www.huoqiu.gov.cn/zwzx/yw/38816107.html (驻外招商联络处调度会)",
        "notes": "毛玲霞，现任霍邱县委常委、副县长。负责招商引资、工业和信息化、人力资源和社会保障、通信等方面工作。",
        "confidence": "confirmed"
    },
    # === 8. Deputy Magistrate (副县长) ===
    {
        "id": 8,
        "name": "刘人淼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（县政府党组成员）",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "刘人淼，现任霍邱县副县长。负责商务工作，协助负责金融监管、巩固拓展脱贫攻坚成果同乡村振兴有效衔接工作。",
        "confidence": "confirmed"
    },
    # === 9. Deputy Magistrate (副县长) ===
    {
        "id": 9,
        "name": "吕彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "吕彬，现任霍邱县副县长。负责农业农村、水利、供销、气象等方面工作。统筹协调长集现代农业产业园工作。",
        "confidence": "confirmed"
    },
    # === 10. Deputy Magistrate (副县长) ===
    {
        "id": 10,
        "name": "刘伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "刘伟，现任霍邱县副县长。负责自然资源、城乡规划、住房城乡建设、交通运输、城市管理、重点工程建设等方面工作。",
        "confidence": "confirmed"
    },
    # === 11. Deputy Magistrate / Public Security (副县长、公安局长) ===
    {
        "id": 11,
        "name": "黄杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "霍邱县公安局",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "黄杰，现任霍邱县副县长、县公安局局长。负责公安、司法、信访、退役军人事务等方面工作。",
        "confidence": "confirmed"
    },
    # === 12. Deputy Magistrate (副县长) ===
    {
        "id": 12,
        "name": "蔡赛虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "蔡赛虎，现任霍邱县副县长。负责科技、地震、数据资源管理、东西湖保护利用、残疾人事业、妇儿等方面工作。",
        "confidence": "confirmed"
    },
    # === 13. Deputy Magistrate (副县长) ===
    {
        "id": 13,
        "name": "杨立发",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（兼高塘镇党委书记）",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "杨立发，现任霍邱县副县长，兼任高塘镇党委书记。负责教育、卫生健康、医疗保障、民政、生态环境保护、文化、旅游、体育等方面工作。",
        "confidence": "confirmed"
    },
    # === 14. Deputy Magistrate (副县长) ===
    {
        "id": 14,
        "name": "王家杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "霍邱县人民政府",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "王家杰，现任霍邱县副县长。负责市场监管、知识产权等方面工作，协助负责招商引资、工业信息化、通信等工作。",
        "confidence": "confirmed"
    },
    # === 15. County Government Chief of Staff (县政府党组成员、办公室主任) ===
    {
        "id": 15,
        "name": "陈正文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、县政府办公室主任",
        "current_org": "霍邱县人民政府办公室",
        "source": "https://www.huoqiu.gov.cn/public/6596251/38800594.html (霍政秘〔2026〕39号)",
        "notes": "陈正文，现任霍邱县政府党组成员、县政府办公室主任。在县长领导下负责处理县政府日常工作，协助负责机关事务管理工作。",
        "confidence": "confirmed"
    },
    # === 16. County People's Congress Chair (县人大常委会主任) ===
    {
        "id": 16,
        "name": "李跃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "霍邱县人民代表大会常务委员会",
        "source": "https://www.huoqiu.gov.cn/zwzx/yw/38813556.html (2026-06-28 县委理论学习中心组学习会); https://www.huoqiu.gov.cn/zwzx/yw/38813847.html (2026-06-28 县人大常委会议)",
        "notes": "李跃，现任霍邱县人大常委会党组书记、主任。",
        "confidence": "confirmed"
    },
    # === 17. County CPPCC Chair (县政协主席) ===
    {
        "id": 17,
        "name": "曹良喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "安徽霍邱",
        "native_place": "安徽霍邱",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政协党组书记、主席",
        "current_org": "霍邱县政协",
        "source": "https://baike.baidu.com/item/%E6%9B%B9%E8%89%AF%E5%96%9C/18800732 (百度百科); https://www.huoqiu.gov.cn/zwzx/yw/38813556.html (2026-06-28 县委理论学习中心组学习会)",
        "notes": "曹良喜，男，汉族，1968年10月生，安徽霍邱人，中共党员，中央党校大学学历。曾任霍邱县城关镇党委副书记、镇长，霍邱县政府副县长、城关镇党委书记，舒城县委常委、政法委书记。2024年11月任霍邱县政协党组书记、主席候选人。现任县委常委、县政协党组书记、主席。",
        "confidence": "confirmed"
    },
    # === 18. Predecessor Party Secretary (前任县委书记) ===
    {
        "id": 18,
        "name": "霍绍斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-08",
        "birthplace": "安徽六安",
        "native_place": "安徽六安",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宿州市委常委、组织部部长",
        "current_org": "中共宿州市委组织部",
        "source": "https://baike.baidu.com/item/%E9%9C%8D%E7%BB%8D%E6%96%8C/8453541 (百度百科); https://www.huoqiu.gov.cn/zwzx/yw/38789149.html (2025-02-13 人武部党委第一书记任职)",
        "notes": "霍绍斌，男，汉族，1971年8月生，安徽六安人，中共党员，中央党校研究生学历。2021年5月至2022年2月任六安市金安区委书记。2022年2月至2025年1月任六安市人大常委会副主任、金安区委书记。2025年1月任六安市委常委、霍邱县委书记。2025年2月兼任霍邱县人武部党委第一书记。后调任宿州市委常委、组织部部长。",
        "confidence": "confirmed"
    },
    # === 19. Predecessor County Magistrate (前任县长) ===
    {
        "id": 19,
        "name": "韦能武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-12",
        "birthplace": "安徽舒城",
        "native_place": "安徽舒城",
        "education": "安徽农业大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（已调离，去向待查）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E9%9F%A6%E8%83%BD%E6%AD%A6/18654755 (百度百科); http://www.hqrd.gov.cn/DocHtml/1/25/12/00003184.html (2025-12-22 县人大常委会接受辞职决定)",
        "notes": "韦能武，男，汉族，1975年12月生，安徽舒城人，中共党员，安徽农业大学兽医专业。2018年4月至2021年1月任叶集区委常委、副区长，区委副书记。2021年6月任霍邱县委副书记，2021年7月任霍邱县人民政府党组书记、代县长，同月正式当选县长。2025年12月22日因工作变动辞去县长职务。目前去向未公开。",
        "confidence": "confirmed"
    },
    # === 20. Cross-county: Qin Fuhao (霍邱籍, 叶集区长) ===
    {
        "id": 20,
        "name": "秦富好",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "安徽霍邱",
        "native_place": "安徽霍邱",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2004-07",
        "current_post": "叶集区委副书记、区长",
        "current_org": "叶集区人民政府",
        "source": "https://www.ahyeji.gov.cn/content/column/6790691?liId=678 (叶集区领导之窗); https://www.ahyeji.gov.cn/public/6596441/26545698.html (2026-05-15 主持区政府第78次常务会议)",
        "notes": "秦富好，男，汉族，安徽霍邱县人，1980年10月出生，2003年2月加入中国共产党，2004年7月参加工作，大学学历。现任叶集区委副书记、区长。领导区政府全面工作，负责审计工作。",
        "confidence": "confirmed"
    },
    # === 21. Cross-county: Xiong Shouhong (霍邱籍, 凤台原书记) ===
    {
        "id": 21,
        "name": "熊寿宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-01",
        "birthplace": "安徽霍邱",
        "native_place": "安徽霍邱",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1991-08",
        "current_post": "淮南市政协副主席",
        "current_org": "淮南市政协",
        "source": "https://baike.baidu.com/item/%E7%86%8A%E5%AF%BF%E5%AE%8F (百度百科)",
        "notes": "熊寿宏，男，汉族，1969年1月生，安徽霍邱人，中共党员。曾任凤台县委书记（2023.09-2026.05），现任淮南市政协副主席（2025.01-）。早期在淮南市田家庵区纪委工作15年。",
        "confidence": "confirmed"
    },
    # === 22. Cross-county: Wang Huadong (霍邱籍, 淮北市委书记) ===
    {
        "id": 22,
        "name": "汪华东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "安徽霍邱",
        "native_place": "安徽霍邱",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淮北市委书记",
        "current_org": "中共淮北市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E6%B7%AE%E5%8C%97%E5%B8%82 (维基百科); 淮北市人民政府官网",
        "notes": "汪华东，男，汉族，1972年11月生，安徽霍邱人，中共党员。曾任淮北市市长（2022.08-2024.09），2024年9月任淮北市委书记。曾为援藏干部。霍邱籍在外最高级别官员（正厅级）。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共霍邱县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共六安市委员会",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 2,
        "name": "霍邱县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "六安市人民政府",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 3,
        "name": "中共霍邱县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共霍邱县委员会",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 4,
        "name": "中共霍邱县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共霍邱县委员会",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 5,
        "name": "霍邱县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "霍邱县人民政府",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 6,
        "name": "霍邱县人民政府办公室",
        "type": "政府",
        "level": "乡科级",
        "parent": "霍邱县人民政府",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 7,
        "name": "霍邱县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "六安市人民代表大会常务委员会",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议霍邱县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协六安市委员会",
        "location": "安徽省六安市霍邱县"
    },
    {
        "id": 9,
        "name": "六安市农业农村局",
        "type": "政府",
        "level": "县处级",
        "parent": "六安市人民政府",
        "location": "安徽省六安市"
    },
    {
        "id": 10,
        "name": "中共六安市金安区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共六安市委员会",
        "location": "安徽省六安市金安区"
    },
    {
        "id": 11,
        "name": "中共宿州市委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共宿州市委员会",
        "location": "安徽省宿州市"
    },
    {
        "id": 12,
        "name": "叶集区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "六安市人民政府",
        "location": "安徽省六安市叶集区"
    },
    {
        "id": 13,
        "name": "中共凤台县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共淮南市委员会",
        "location": "安徽省淮南市凤台县"
    },
    {
        "id": 14,
        "name": "淮南市政协",
        "type": "政协",
        "level": "厅局级",
        "parent": "政协安徽省委员会",
        "location": "安徽省淮南市"
    },
    {
        "id": 15,
        "name": "中共淮北市委员会",
        "type": "党委",
        "level": "厅局级",
        "parent": "中共安徽省委员会",
        "location": "安徽省淮北市"
    },
    {
        "id": 16,
        "name": "中共叶集区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共六安市委员会",
        "location": "安徽省六安市叶集区"
    },
]

positions = [
    # Person 1: 高宗保
    {"person_id": 1, "org_id": 9, "title": "六安市委农办主任、市农业农村局党组书记、局长", "start": "2022-11", "end": "2026-04", "rank": "正处级", "note": "任职约3年5个月"},
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026年4月23日公示，5月正式就任"},
    # Person 2: 沈勇
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start": "2025-12", "end": "2026-01", "rank": "正处级", "note": "2025年12月22日任命为代理县长"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "2026-01", "end": "present", "rank": "正处级", "note": "2026年1月14日正式当选"},
    # Person 3: 朱成亮
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present", "rank": "副处级", "note": "履历待查"},
    # Person 4: 王竹
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "履历待查"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": "县委常委屈"},
    # Person 5: 周尚
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start": "unknown", "end": "present", "rank": "副处级", "note": "履历待查"},
    {"person_id": 5, "org_id": 3, "title": "政法委书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 6: 任长虹
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "履历待查"},
    {"person_id": 6, "org_id": 4, "title": "宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 7: 毛玲霞
    {"person_id": 7, "org_id": 2, "title": "县委常委、副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 8-14: Deputy Magistrates
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "刘人淼"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "吕彬"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "刘伟"},
    {"person_id": 11, "org_id": 2, "title": "副县长、县公安局局长", "start": "unknown", "end": "present", "rank": "副处级", "note": "黄杰"},
    {"person_id": 11, "org_id": 5, "title": "县公安局局长", "start": "unknown", "end": "present", "rank": "乡科级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "蔡赛虎"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "杨立发"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": "王家杰"},
    # Person 15: 陈正文
    {"person_id": 15, "org_id": 6, "title": "县政府党组成员、办公室主任", "start": "unknown", "end": "present", "rank": "乡科级", "note": ""},
    # Person 16: 李跃
    {"person_id": 16, "org_id": 7, "title": "县人大常委会党组书记、主任", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    # Person 17: 曹良喜
    {"person_id": 17, "org_id": 8, "title": "县政协党组书记、主席", "start": "2024-11", "end": "present", "rank": "正处级", "note": "2024年11月21日任党组书记、主席候选人"},
    {"person_id": 17, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 18: 霍绍斌
    {"person_id": 18, "org_id": 10, "title": "六安市金安区委书记", "start": "2021-05", "end": "2025-01", "rank": "正处级", "note": "2022.02起同时任六安市人大常委会副主任"},
    {"person_id": 18, "org_id": 1, "title": "县委书记（六安市委常委兼）", "start": "2025-01", "end": "2026-04", "rank": "副厅级", "note": "六安市委常委、霍邱县委书记"},
    {"person_id": 18, "org_id": 11, "title": "宿州市委常委、组织部部长", "start": "2026-04", "end": "present", "rank": "副厅级", "note": "调任"},
    # Person 19: 韦能武
    {"person_id": 19, "org_id": 2, "title": "县长", "start": "2021-07", "end": "2025-12", "rank": "正处级", "note": "2021年7月任代县长，同月当选；2022年1月连任"},
    {"person_id": 19, "org_id": 1, "title": "县委副书记", "start": "2021-06", "end": "2025-12", "rank": "副处级", "note": ""},
    # Person 20: 秦富好
    {"person_id": 20, "org_id": 12, "title": "叶集区委副书记、区长", "start": "unknown", "end": "present", "rank": "正处级", "note": "霍邱籍，六安市内跨县交流"},
    # Person 21: 熊寿宏
    {"person_id": 21, "org_id": 13, "title": "凤台县委书记", "start": "2023-09", "end": "2026-05", "rank": "正处级", "note": "霍邱出生，跨市交流至淮南"},
    {"person_id": 21, "org_id": 14, "title": "淮南市政协副主席", "start": "2025-01", "end": "present", "rank": "副厅级", "note": "2025年1月起兼任，2026年5月后专职"},
    # Person 22: 汪华东
    {"person_id": 22, "org_id": 15, "title": "淮北市委书记", "start": "2024-09", "end": "present", "rank": "正厅级", "note": "霍邱籍在外最高职务"},
]

relationships = [
    # Core team: 高宗保 + 沈勇
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长，霍邱县党政主要领导搭档", "overlap_org": "霍邱县", "overlap_period": "2026-05至今"},
    # 高宗保 + 朱成亮
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共霍邱县委员会", "overlap_period": "2026-05至今"},
    # 高宗保 + 王竹
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委、常务副县长", "overlap_org": "霍邱县", "overlap_period": "2026-05至今"},
    # 高宗保 + 曹良喜
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate", "context": "县委书记与县政协主席", "overlap_org": "霍邱县", "overlap_period": "2026-05至今"},
    # 沈勇 + 王竹 (政府班子搭档)
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "霍邱县人民政府", "overlap_period": "2025-12至今"},
    # 沈勇 + 朱成亮
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记", "overlap_org": "霍邱县", "overlap_period": "2025-12至今"},
    # 高宗保 + 霍绍斌 (前后任)
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "霍绍斌调任宿州后，高宗保接任县委书记", "overlap_org": "中共霍邱县委员会", "overlap_period": "2026-04/05 交接"},
    # 沈勇 + 韦能武 (前后任)
    {"person_a": 2, "person_b": 19, "type": "predecessor_successor", "context": "韦能武辞职后，沈勇接任县长", "overlap_org": "霍邱县人民政府", "overlap_period": "2025-12 交接"},
    # 霍绍斌 + 韦能武 (曾搭档)
    {"person_a": 18, "person_b": 19, "type": "overlap", "context": "霍绍斌任县委书记时，韦能武任县长", "overlap_org": "霍邱县", "overlap_period": "2025-01至2025-12"},
    # 秦富好（霍邱籍）- 霍邱县地缘关系
    {"person_a": 20, "person_b": 1, "type": "same_native_place", "context": "秦富好为霍邱籍，与高宗保在霍邱县有工作交集", "overlap_org": "", "overlap_period": ""},
    {"person_a": 20, "person_b": 2, "type": "same_native_place", "context": "秦富好为霍邱籍，沈勇为霍邱县长", "overlap_org": "", "overlap_period": ""},
    # 熊寿宏（霍邱籍）- 地缘
    {"person_a": 21, "person_b": 1, "type": "same_native_place", "context": "熊寿宏为霍邱出生，高宗保为霍邱县委书记", "overlap_org": "", "overlap_period": ""},
    # 汪华东（霍邱籍）- 地缘
    {"person_a": 22, "person_b": 1, "type": "same_native_place", "context": "汪华东为霍邱人，霍邱籍在外最高级别官员", "overlap_org": "", "overlap_period": ""},
    {"person_a": 22, "person_b": 2, "type": "same_native_place", "context": "汪华东为霍邱人，与沈勇为同籍", "overlap_org": "", "overlap_period": ""},
]


def build_db():
    """Create and populate SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, native_place TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                native_place, education, party_join, work_start,
                current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"],
              p["current_post"], p["current_org"],
              p["source"], p["notes"], p["confidence"]))

    # Insert organizations
    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    # Insert relationships
    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' for a person based on role."""
    post = p.get("current_post", "")
    name = p.get("name", "")
    if "书记" in post and "县委" in post:
        return "255,50,50"
    elif "县长" in post or "区长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "政法委" in post:
        return "255,165,0"
    elif "政协" in post:
        return "200,255,255"
    elif "人大" in post:
        return "200,255,255"
    else:
        return "100,100,100"


def build_gexf():
    """Generate GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>霍邱县领导班子工作关系网络 - 中共霍邱县委、霍邱县人民政府领导班子成员及跨县交流关系</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        is_top = any(kw in p["current_post"] for kw in ["县委书记", "县长", "区长"])
        sz = "20.0" if is_top else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    for o in organizations:
        c = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    eid = 0
    lines.append('    <edges>')

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        w = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} → {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("\n── Summary ────────────────────────────────────────────────────")
    c.execute("SELECT COUNT(*) FROM persons")
    print(f"  Persons: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Organizations: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM positions")
    print(f"  Positions: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Relationships: {c.fetchone()[0]}")

    print("\n  Top leaders:")
    c.execute("SELECT name, current_post FROM persons WHERE id IN (1,2)")
    for row in c.fetchall():
        print(f"    {row[0]} — {row[1]}")

    print("\n  Deputy leaders:")
    c.execute("SELECT name, current_post FROM persons WHERE id IN (3,4,5,6,7)")
    for row in c.fetchall():
        print(f"    {row[0]} — {row[1]}")

    print("\n  Government deputies:")
    c.execute("SELECT name, current_post FROM persons WHERE id IN (8,9,10,11,12,13,14)")
    for row in c.fetchall():
        print(f"    {row[0]} — {row[1]}")

    print("\n  Cross-county connections:")
    c.execute("SELECT name, current_post, birthplace FROM persons WHERE id IN (20,21,22)")
    for row in c.fetchall():
        print(f"    {row[0]} ({row[2] or '?'}) — {row[1]}")

    conn.close()


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()

    print(f"\n── Files ─────────────────────────────────────────────────────")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("✅ Done.")
