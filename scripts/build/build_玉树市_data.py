#!/usr/bin/env python3
"""玉树市（青海省玉树藏族自治州）市委书记、市长领导班子工作关系网络数据构建脚本。

数据来源（截至 2026-08-01）：
- 玉树市人民政府官网 www.yushushi.gov.cn（一手权威来源）
  - 本地要闻：中国共产党玉树市第四届委员会第一次全体会议（2026-08-01，四届市委班子诞生）
  - 玉树市第四届人民代表大会第一次会议（2026-07-30，代市长却洛作政府工作报告）
  - 谭晟、却洛在"七一"前夕开展走访慰问（2026-07-01，确认"州委常委、玉树市委书记谭晟，市人民政府党组书记却洛"）
  - 谭晟、却洛赴国营牧场调研（2026-07-01）
  - 玉树市委书记谭晟主持召开市委常委会会议（2026-08-01）
  - 政府信息公开>机关简介>政府领导（政府班子成员名单/分工）
  - 罗东川在玉树州玉树市调研（2026-08-01，省长调研）
  - 马锐分别拜会省司法厅财政厅（2026-07-02，州委书记马锐）
- 备注：
  - 谭晟、却洛的出生/学历/入党时间及早年履历，公开源未收录（Bing/Baidu/Jina/Exa 在本次会话中被反爬或超时，未取到百科资料），以 open_questions 标注。
  - 前任市委书记（第三届委员会书记）姓名/去向、却洛此前确切职务、扎西旺加卸任去向 待补。

生成产物：data/database/玉树市_network.db + data/graph/玉树市_network.gexf
"""

import os
import sqlite3  # noqa: F401  (含于标准库，供脚本校验 DB；数据写入由 run_build 完成)

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── 路径（规范目标：data/database、data/graph）──
DB_PATH = DATABASE_DIR / "玉树市_network.db"
GEXF_PATH = GRAPH_DIR / "玉树市_network.gexf"

# ── 人员（id 为整数，positions/relationships 用同一整数引用）──
# 1-2 现任核心；3-13 四届市委班子；14-20 政府班子；21 人大；22-24 州/省上级
persons = [
    # ===== 现任核心（confirmed，市政府官网 2026-08-01 截至）=====
    {
        "id": 1, "name": "谭晟", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "玉树市委书记（州委常委兼任）", "current_org": "中共玉树市委员会",
        # 2026-06-30 "州委常委、玉树市委书记谭晟"活动；2026-07-21 当选四届市委书记；2026-07-27 主持市委常委会
        "source": "http://www.yushushi.gov.cn/html/3346/627023.html",
    },
    {
        "id": 2, "name": "却洛", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "玉树市委副书记、代理市长", "current_org": "玉树市人民政府",
        # 2026-06-30 市人民政府党组书记；2026-07-29 四届人大会议作为代理市长作政府工作报告
        "source": "http://www.yushushi.gov.cn/html/3346/627033.html",
    },
    # ===== 前任市长 =====
    {
        "id": 3, "name": "扎西旺加", "gender": "男", "birth": "1973-09", "education": "大学",
        "current_post": "〔前任〕玉树市委副书记、市长（约2021-2026）", "current_org": "玉树市人民政府",
        # 官网机关简介（2023-10-10）：男，藏族，青海囊谦人，中共党员，大学学历，1973-09 生，
        # 1992-07 参加工作，1997-12 入党，任市委副书记、市政府党组书记、市长
        "source": "http://www.yushushi.gov.cn/html/3495/623584.html",
    },
    # ===== 四届市委班子（2026-07-21 四届一次全会，confirmed）=====
    {"id": 4, "name": "扎西尼玛", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市委副书记", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    {"id": 5, "name": "顾祥林", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市委副书记", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    {"id": 6, "name": "洛桑才仁", "gender": "待查", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    {"id": 7, "name": "扎西巴旦", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委、副市长", "current_org": "玉树市人民政府",
     # 既是市委常委又是副市长（兼农牧/乡村振兴/交通/水利/科技），双职
     "source": "http://www.yushushi.gov.cn/html/3495/314216.html"},
    {"id": 8, "name": "斯慧兰", "gender": "女", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    {"id": 9, "name": "更秋其梅", "gender": "待查", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    {"id": 10, "name": "才仁旺加", "gender": "待查", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    {"id": 11, "name": "刘挺", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委", "current_org": "中共玉树市委员会",
     # 四届人大会议主席台前排就座（2026-07-29）
     "source": "http://www.yushushi.gov.cn/html/3346/627033.html"},
    {"id": 12, "name": "李振彬", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    {"id": 13, "name": "当周尖措", "gender": "待查", "birth": "待查", "education": "待查",
     "current_post": "玉树市委常委", "current_org": "中共玉树市委员会",
     "source": "http://www.yushushi.gov.cn/html/3346/627038.html"},
    # ===== 政府班子（机关简介·政府领导，confirmed）=====
    {
        "id": 14, "name": "冯玉林", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "玉树市常务副市长", "current_org": "玉树市人民政府",
        # 负责市政府日常工作，分管人社/发改/财政/统计/应急等
        "source": "http://www.yushushi.gov.cn/html/3495/623586.html",
    },
    {"id": 15, "name": "赵昭", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市副市长（援青干部）", "current_org": "玉树市人民政府",
     "source": "http://www.yushushi.gov.cn/html/3495/626488.html"},
    {"id": 16, "name": "陈稳", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市副市长（援青干部）", "current_org": "玉树市人民政府",
     "source": "http://www.yushushi.gov.cn/html/3495/626489.html"},
    {"id": 17, "name": "洛吾扎巴", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市副市长、公安局长", "current_org": "玉树市公安局",
     "source": "http://www.yushushi.gov.cn/html/3495/314213.html"},
    {"id": 18, "name": "永措", "gender": "女", "birth": "待查", "education": "待查",
     "current_post": "玉树市副市长", "current_org": "玉树市人民政府",
     # 负责民政、退役军人、教育、卫健、医保、文体旅等
     "source": "http://www.yushushi.gov.cn/html/3495/314215.html"},
    {"id": 19, "name": "开周才仁", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市副市长", "current_org": "玉树市人民政府",
     "source": "http://www.yushushi.gov.cn/html/3495/623588.html"},
    {"id": 20, "name": "久扎西", "gender": "男", "birth": "待查", "education": "待查",
     "current_post": "玉树市副市长（2026-04 候选人）", "current_org": "玉树市人民政府",
     "source": "http://www.yushushi.gov.cn/html/3495/626965.html"},
    # ===== 人大 =====
    {
        "id": 21, "name": "汤有然", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "玉树市人大常委会主任", "current_org": "玉树市人民代表大会常务委员会",
        # 四届人大第一次会议主持人、大会执行主席（2026-07-29）
        "source": "http://www.yushushi.gov.cn/html/3346/627033.html",
    },
    # ===== 州/省上级（监督与调研链）=====
    {
        "id": 22, "name": "马锐", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "玉树州委书记", "current_org": "中共玉树藏族自治州委员会",
        # 2026-05 在玉树市调研强调绿色发展；2026-06/07 拜东省司法厅财政厅
        "source": "http://www.yushushi.gov.cn/html/3346/627011.html",
    },
    {
        "id": 23, "name": "罗东川", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "青海省委副书记、省长", "current_org": "青海省人民政府",
        # 2026-07-24/25 调研玉树市，出席三江源生态文化旅游节开幕
        "source": "http://www.yushushi.gov.cn/html/3346/627035.html",
    },
    {
        "id": 24, "name": "龙措", "gender": "待查", "birth": "待查", "education": "待查",
        "current_post": "玉树州长、州委副书记", "current_org": "玉树藏族自治州人民政府",
        # 玉树州长/州委副书记（杂多县任务核实）；赴杂多督导
        "source": "http://www.zaduo.gov.cn",
    },
]

# ── 组织 ──
organizations = [
    {"id": 1, "name": "中共玉树市委员会", "type": "党委", "level": "县级", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 2, "name": "玉树市人民政府", "type": "政府", "level": "县级", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 3, "name": "中共玉树市纪律检查委员会", "type": "党委", "level": "县级", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 4, "name": "玉树市人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 5, "name": "玉树市公安局", "type": "政府", "level": "县级", "location": "青海省玉树藏族自治州玉树市"},
    {"id": 6, "name": "中共玉树藏族自治州委员会", "type": "党委", "level": "地级", "location": "青海省玉树藏族自治州"},
    {"id": 7, "name": "玉树藏族自治州人民政府", "type": "政府", "level": "地级", "location": "青海省玉树藏族自治州"},
    {"id": 8, "name": "青海省人民政府", "type": "政府", "level": "省级", "location": "青海省西宁市"},
]

# ── 任职 ──
positions = [
    # 现任核心
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2026-07"},
    {"person_id": 1, "org_id": 6, "title": "州委常委（兼任）", "start": "2026?"},
    {"person_id": 2, "org_id": 2, "title": "代理市长", "start": "2026-07"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2026-07"},
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记", "start": "2026-06"},
    # 前任市长
    {"person_id": 3, "org_id": 2, "title": "市委副书记、市政府、市长", "start": "2021?", "end": "2026"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "2021?", "end": "2026"},
    # 四届市委班子
    {"person_id": 4, "org_id": 1, "title": "市委副书记", "start": "2026-07"},
    {"person_id": 5, "org_id": 1, "title": "市委副书记", "start": "2026-07"},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    {"person_id": 7, "org_id": 2, "title": "副市长（分管农牧、交通、水利、科技）", "start": "2021", "end": "present"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    {"person_id": 13, "org_id": 1, "title": "市委常委", "start": "2026-07"},
    # 政府班子
    {"person_id": 14, "org_id": 2, "title": "常务副市长", "start": "2024?"},
    {"person_id": 15, "org_id": 2, "title": "副市长（援青）", "start": "2023?"},
    {"person_id": 16, "org_id": 2, "title": "副市长（援青）", "start": "2023?"},
    {"person_id": 17, "org_id": 2, "title": "副市长、公安局长", "start": "2021?"},
    {"person_id": 17, "org_id": 5, "title": "公安局长", "start": "2021?"},
    {"person_id": 18, "org_id": 2, "title": "副市长", "start": "2021?"},
    {"person_id": 19, "org_id": 2, "title": "副市长", "start": "2023?"},
    {"person_id": 20, "org_id": 2, "title": "副市长候选人", "start": "2026-04"},
    # 人大
    {"person_id": 21, "org_id": 4, "title": "市人大常委会主任", "start": "2021?"},
    # 州/省上级
    {"person_id": 22, "org_id": 6, "title": "州委书记", "start": "2025?"},
    {"person_id": 23, "org_id": 8, "title": "省委副书记、省长", "start": "2025?"},
    {"person_id": 24, "org_id": 7, "title": "州长、州委副书记", "start": "2025?"},
]

# ── 关系 ──
relationships = [
    # 现任党政一把手搭档
    {
        "person_a": 1, "person_b": 2, "type": "党政搭档",
        "context": "市委书记与代市长（党政一把手搭档），共同慰问老党员、七一走访、赴国营牧场调研",
        "overlap_org": "玉树市（市委/市政府）", "overlap_period": "2026 至今",
    },
    # 上下级（市长与副市长）
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "代市长与常务副市长（政府核心搭档）", "overlap_org": "玉树市人民政府"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "代市长与副市长（援青）", "overlap_org": "玉树市人民政府"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "代市长与副市长（援青）", "overlap_org": "玉树市人民政府"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "代市长与副市长、公安局长", "overlap_org": "玉树市人民政府"},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "代市长与副市长", "overlap_org": "玉树市人民政府"},
    {"person_a": 2, "person_b": 19, "type": "上下级", "context": "代市长与副市长", "overlap_org": "玉树市人民政府"},
    # 市委书记与市委副书记（党口）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记与市委副书记", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记与市委副书记", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "市委书记与市委副书记（代市长）", "overlap_org": "中共玉树市委员会"},
    # 前后任市长
    {
        "person_a": 3, "person_b": 2, "type": "前后任",
        "context": "扎西旺加（市长，2021?-2026）→ 却洛（代理市长 2026-07），四届人大换届交接",
        "overlap_org": "玉树市人民政府", "overlap_period": "2026",
    },
    # 州—市上下级工作关系
    {
        "person_a": 22, "person_b": 1, "type": "州市级领导上下级",
        "context": "州委书记马旭在玉树市调研强调把绿色发展作为树立正确政绩观的重要取向，指导市委书记",
        "overlap_org": "玉树藏族自治州/玉树市",
    },
    {
        "person_a": 22, "person_b": 2, "type": "州县长下级",
        "context": "州委书记马旭领导代市长却洛的市政府工作",
        "overlap_org": "玉树藏族自治州/玉树市",
    },
    {
        "person_a": 23, "person_b": 1, "type": "省级市县领导上下级",
        "context": "省长罗东川2026-07-24/25调研玉树市，市委书记谭成学习贯彻其讲话精神并主持召开常委会部署",
        "overlap_org": "青海省/玉树市",
    },
    {
        "person_a": 23, "person_b": 2, "type": "省级市县领导上下级",
        "context": "省长罗东川调研玉树市，对市政府工作提出要求（虫草产业、牦牛、草原修复等）",
        "overlap_org": "青海省/玉树市",
    },
    {
        "person_a": 24, "person_b": 2, "type": "州县长下级",
        "context": "州长龙措与玉树市代市长工作对接（州政府领导县级市）",
        "overlap_org": "玉树藏族自治州/玉树市",
    },
    # 常委会内部协作
    {"person_a": 1, "person_b": 6, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 7, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 8, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 9, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 10, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 11, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 12, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    {"person_a": 1, "person_b": 13, "type": "同级", "context": "市委常委班子", "overlap_org": "中共玉树市委员会"},
    # 人大与党委/政府关系
    {"person_a": 21, "person_b": 1, "type": "人大党委关系", "context": "市人大常委会主任汤有然主持四届人大一次会议，执行主席含市委书记", "overlap_org": "玉树市"},
]

# ── 构建 ──
if __name__ == "__main__":
    run_build(
        slug="玉树市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"✅ 数据库: {DB_PATH}")
    print(f"✅ 图文件: {GEXF_PATH}")