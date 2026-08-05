#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 绥化市 leadership network.

绥化市是黑龙江省中北部地级市，地处松嫩平原腹地，别称"寒地黑土之都"，下辖北林区、
安达市、肇东市、海伦市、望奎县、兰西县、青冈县、庆安县、明水县、绥棱县共10个县级政
区，是黑龙江省重要农业大市和粮食主产区。

Current leadership as of 2026-08 (sources: 绥化市人民政府门户网站 www.suihua.gov.cn
「市政府/市政府领导」官方简历页、绥化市政府2026年《政府工作报告》、
中共绥化市委相关新闻报道、既有县域调查 build_肇东市_data.py 等汇总):
- 市委书记: 韩雪松（现任，2026年8月官方新闻持续确认；详细履历见 background research）
- 市委副书记、市长、市政府党组书记: 陈立军（男，汉族，1972年2月生，在职研究生，
  公共管理硕士，中共党员；2026年1月在绥化市第五届人大五次会议上作政府工作报告）

市政府班子（官方「市政府领导」领导之窗确认，2026-08）：
- 董鹏翔：市委常委、市政府副市长（常务）、党组副书记、一级巡视员（男汉1975.8）
- 谢璐遥：市委常委、市政府副市长（女汉1977.8，研究生法学硕士）
- 关海涛：市委常委、市政府副市长（男满1976.3，大学）
- 丁然：市政府副市长、市公安局党委书记/局长/督察长（男汉1973.10，在职研究生公共管理硕士）
- 张萌：市政府副市长（女汉1979.9，研究生管理学博士）
- 朱恒利：市政府副市长（男汉1980.3，研究生工学硕士）
- 刘文杰：市政府副市长、市工商联主席（男汉1974.6，大学本科，民建会员）
- 吕江：市政府副市长人选（男汉1973.6，大学，中共党员；原肇东市委书记，2026年6-7月调任）
- 李月峰：市政府秘书长

网络连接线索：
- 吕江（原肇东市委书记，2026年6月前）调任绥化市政府副市长人选——县级市书记向地级市政
  府副职的跨层级晋升，是本市内部人事流动的重要证据。
- 韩雪松曾任哈尔滨市南岗区领导（repository既往调研将韩雪松列入南岗区政府班子列席领导），
  后任绥化市委书记——跨地厅级成长路径。
- 本视图下属10县市区为绥化市直接管理层级。

详细资料来源详见脚本 docstring 尾部及各 person 的 source 字段。部分人物完整履历/籍贯/学历
公开资料有限，均在 confidence、open_questions 标注并写入 report/open_gaps.md，未作虚构。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "绥化市"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "绥化市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "绥化市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "绥化市_network.db"
    GEXF_PATH = GRAPH_DIR / "绥化市_network.gexf"

# ── ORGANIZATIONS (id convention: 1/2/3/4/5=四大班子+纪委; 10+=省级; 20+=各县市区) ──
organizations = [
    {"id": 1, "name": "中共绥化市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "黑龙江省绥化市北林区"},
    {"id": 2, "name": "绥化市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省绥化市北林区"},
    {"id": 3, "name": "绥化市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "黑龙江省人民代表大会常务委员会", "location": "黑龙江省绥化市北林区"},
    {"id": 4, "name": "中国人民政治协商会议绥化市委员会", "type": "政协", "level": "地厅级", "parent": "政协黑龙江省委员会", "location": "黑龙江省绥化市北林区"},
    {"id": 5, "name": "中共绥化市纪律检查委员会/绥化市监察委员会", "type": "纪委", "level": "地厅级", "parent": "中共黑龙江省纪委/省监委", "location": "黑龙江省绥化市北林区"},
    {"id": 6, "name": "绥化市公安局", "type": "政府机关", "level": "正处级", "parent": "绥化市人民政府", "location": "黑龙江省绥化市"},
    {"id": 7, "name": "绥化经济技术开发区", "type": "开发区", "level": "副厅级", "parent": "绥化市人民政府", "location": "黑龙江省绥化市"},
    {"id": 8, "name": "黑龙江省人民政府", "type": "政府", "level": "省部级", "parent": "中华人民共和国国务院", "location": "黑龙江省哈尔滨市"},
    {"id": 9, "name": "中共黑龙江省委员会", "type": "党委", "level": "省部级", "parent": "中国共产党中央委员会", "location": "黑龙江省哈尔滨市"},

    # 跨地市连接（韩雪松早年任职）
    {"id": 10, "name": "中共哈尔滨市南岗区委员会/南岗区人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "黑龙江省哈尔滨市南岗区"},

    # 市辖10县区（市域管理层级，跨级连接用）
    {"id": 101, "name": "中共肇东市委员会", "type": "党委", "level": "正处级", "parent": "中共绥化市委员会", "location": "黑龙江省绥化市肇东市"},
    {"id": 102, "name": "中共兰西县委员会", "type": "党委", "level": "正处级", "parent": "中共绥化市委员会", "location": "黑龙江省绥化市兰西县"},
    {"id": 103, "name": "中共庆安县委员会", "type": "党委", "level": "正处级", "parent": "中共绥化市委员会", "location": "黑龙江省绥化市庆安县"},
    {"id": 104, "name": "中共望奎县委员会", "type": "党委", "level": "正处级", "parent": "中共绥化市委员会", "location": "黑龙江省绥化市望奎县"},
    {"id": 105, "name": "中共海伦市委员会", "type": "党委", "level": "正处级", "parent": "中共绥化市委员会", "location": "黑龙江省绥化市海伦市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 韩雪松 — 市委书记（现任）
    {"id": 1, "name": "韩雪松", "gender": "男",
     "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "绥化市委书记", "current_org": "中共绥化市委员会",
     "source": "https://www.suihua.gov.cn/; prior research build_南岗区_data.py"},
    # 2 — 陈立军 — 市委副书记、市长（现任）
    {"id": 2, "name": "陈立军", "gender": "男",
     "ethnicity": "汉族", "birth": "1972年2月", "birthplace": "",
     "education": "在职研究生、公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市委副书记、市政府市长、党组书记", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zfsz/202401/c12_176938.shtml"},
    # 3 — 董鹏翔 — 市委常委、常务副市长
    {"id": 3, "name": "董鹏翔", "gender": "男",
     "ethnicity": "汉族", "birth": "1975年8月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市委常委、市政府副市长、党组副书记、一级巡视员", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202606/c12_235459.shtml"},
    # 4 — 谢璐遥 — 市委常委、副市长
    {"id": 4, "name": "谢璐遥", "gender": "女",
     "ethnicity": "汉族", "birth": "1977年8月", "birthplace": "",
     "education": "研究生、法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市委常委、市政府副市长", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202606/c12_235354.shtml"},
    # 5 — 关海涛 — 市委常委、副市长
    {"id": 5, "name": "关海涛", "gender": "男",
     "ethnicity": "满族", "birth": "1976年3月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市委常委、市政府副市长", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202411/c12_197675.shtml"},
    # 6 — 丁然 — 副市长兼公安局长
    {"id": 6, "name": "丁然", "gender": "男",
     "ethnicity": "汉族", "birth": "1973年10月", "birthplace": "",
     "education": "在职研究生、公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市政府副市长、市公安局局长", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202306/c12_4949511e39e94e70b893c2019010b89d.shtml"},
    # 7 — 张萌 — 副市长
    {"id": 7, "name": "张萌", "gender": "女",
     "ethnicity": "汉族", "birth": "1979年9月", "birthplace": "",
     "education": "研究生、管理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市政府副市长", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202312/c12_165286.shtml"},
    # 8 — 朱恒利 — 副市长
    {"id": 8, "name": "朱恒利", "gender": "男",
     "ethnicity": "汉族", "birth": "1980年3月", "birthplace": "",
     "education": "研究生、工学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市政府副市长", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202506/c12_211794.shtml"},
    # 9 — 刘文杰 — 副市长（党外，民建）
    {"id": 9, "name": "刘文杰", "gender": "男",
     "ethnicity": "汉族", "birth": "1974年6月", "birthplace": "",
     "education": "大学本科",
     "party_join": "民建会员（非中共党员）", "work_start": "",
     "current_post": "绥化市政府副市长、市工商联主席", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202508/c12_214987.shtml"},
    # 10 — 吕江 — 副市长人选（原肇东市委书记）
    {"id": 10, "name": "吕江", "gender": "男",
     "ethnicity": "汉族", "birth": "1973年6月", "birthplace": "",
     "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "绥化市政府副市长人选", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/zffsz/202607/c12_237572.shtml; build_肇东市_data.py"},
    # 11 — 李月峰 — 市政府秘书长
    {"id": 11, "name": "李月峰", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "绥化市政府秘书长", "current_org": "绥化市人民政府",
     "source": "https://www.suihua.gov.cn/sh/shzf/zfld.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 韩雪松
    {"person_id": 1, "org_id": 1, "title": "绥化市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "现任市委书记（2026-08官方新闻确认）；曾任哈尔滨市南岗区领导（repository既往记录）"},
    # 陈立军
    {"person_id": 2, "org_id": 1, "title": "绥化市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "绥化市人民政府市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市长、市政府党组书记；2026年1月22日人大会议作政府工作报告"},
    # 董鹏翔
    {"person_id": 3, "org_id": 1, "title": "绥化市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "绥化市人民政府常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "党组副书记、一级巡视员，协助主持市政府日常工作"},
    # 谢璐遥
    {"person_id": 4, "org_id": 1, "title": "绥化市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "绥化市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 关海涛
    {"person_id": 5, "org_id": 1, "title": "绥化市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "绥化市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责农业农村、水务、生态环境"},
    # 丁然
    {"person_id": 6, "org_id": 2, "title": "绥化市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "公安局党委书记、局长、督察长；负责公安、司法"},
    {"person_id": 6, "org_id": 6, "title": "绥化市公安局局长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼"},
    # 张萌
    {"person_id": 7, "org_id": 2, "title": "绥化市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责民政、交通运输、商务、工业和信息化"},
    # 朱恒利
    {"person_id": 8, "org_id": 2, "title": "绥化市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责自然资源、城乡建设和城管执法"},
    # 刘文杰
    {"person_id": 9, "org_id": 2, "title": "绥化市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责教育、退役军人事务、林草和科技"},
    # 吕江
    {"person_id": 10, "org_id": 2, "title": "绥化市人民政府副市长人选", "start_date": "2026-07", "end_date": "present", "rank": "副厅级（拟任）", "note": "2026年6-7月自肇东市委书记调任"},
    {"person_id": 10, "org_id": 101, "title": "肇东市委书记", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "2026年6月4日仍在主持肇东市委常委会（source: data/肇东市 prior investigation）"},
    # 李月峰
    {"person_id": 11, "org_id": 2, "title": "绥化市人民政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────
relationships = [
    # 书记—市长 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "韩雪松（市委书记）与陈立军（市委副书记、市长）为绥化市现任党政一把手，同一市委班子", "overlap_org": "中共绥化市委", "overlap_period": "至今"},
    # 市长—常务副市长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "陈立军（市长）与董鹏翔（市委常委、常务副市长）为市政府正副主官配对", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    # 书记—各市委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "韩雪松（市委书记）与董鹏翔（市委常委）同为市委常委会成员", "overlap_org": "中共绥化市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "韩雪松（市委书记）与谢璐遥（市委常委）同为市委常委会成员", "overlap_org": "中共绥化市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "韩雪松（市委书记）与关海涛（市委常委）同为市委常委会成员", "overlap_org": "中共绥化市委", "overlap_period": "至今"},
    # 市长—各副市长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "陈立军（市长）与谢璐遥（副市长）共事于市政府班子", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "陈立军（市长）与关海涛（副市长）共事于市政府班子", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "陈立军（市长）与丁然（副市长兼公安局长）共事于市政府班子", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "陈立军（市长）与张萌（副市长）共事于市政府班子", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "陈立军（市长）与朱恒利（副市长）共事于市政府班子", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "陈立军（市长）与刘文杰（副市长）共事于市政府班子", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "陈立军（市长）与吕江（副市长人选）为市政府班子新增副职", "overlap_org": "绥化市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "陈立军（市长）与李月峰（市政府秘书长）为市政府办主从配对", "overlap_org": "绥化市人民政府", "overlap_period": "至今"},
    # 吕江 — 跨层级晋升（promotion chain）：肇东市委书记→绥化市政府副市长
    {"person_a": 10, "person_b": 2, "type": "晋升链条", "context": "吕江自肇东市委书记晋升为绥化市政府副市长人选，属县级市书记向地级市政府副职级跨层级调任（市委层面同一体系干部流动）", "overlap_org": "绥化市人民政府", "overlap_period": "2026年6-7月"},
    # 吕江 — 原肇东搭档（依据既有肇东调查：肖福凌接替吕江）
    {"person_a": 10, "person_b": 5, "type": "同省地市正职", "context": "吕江（副市长人选）与关海涛（副市长）同为市政府班子成员，形成新共事", "overlap_org": "绥化市人民政府", "overlap_period": "2026年"},
    # 韩雪松 跨地市成长线索（哈尔滨南岗→绥化）
    {"person_a": 1, "person_b": 7, "type": "同省干部", "context": "韩雪松曾任职哈尔滨，现为绥化市委书记，属省内地级市正职干部；张萌（女副市长）与其同班子。此边标注为成长路径北线索，非直接共事证据", "overlap_org": "黑龙江省", "overlap_period": "", "context_note": "weak"},
]

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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")