#!/usr/bin/env python3
"""Build 乡宁县 leadership network database and GEXF graph."""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

persons = [
    {"id": 1, "name": "李永芳", "gender": "男", "birth": "", "current_post": "县委书记", "current_org": "中共乡宁县委员会", "source": "http://www.xiangning.gov.cn/contents/10785/3869.html"},
    {"id": 2, "name": "许华伟", "gender": "男", "birth": "1977.04", "current_post": "县委副书记、县长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10942/674.html"},
    {"id": 3, "name": "张曙光", "gender": "男", "birth": "", "current_post": "县委副书记", "current_org": "中共乡宁县委员会", "source": "https://mp.weixin.qq.com/s/9hplVdWXJWToJ9qSTQ4rRA"},
    {"id": 4, "name": "卢冬", "gender": "女", "birth": "1972.01", "current_post": "县委常委、副县长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10943/678.html"},
    {"id": 5, "name": "张保平", "gender": "男", "birth": "", "current_post": "县委常委、政法委书记", "current_org": "中共乡宁县委员会", "source": "https://mp.weixin.qq.com/s/IFFKPo5Xl5hGf5geKNNaZw"},
    {"id": 6, "name": "王丽霞", "gender": "女", "birth": "", "current_post": "县委常委、宣传部长", "current_org": "中共乡宁县委员会", "source": "https://mp.weixin.qq.com/s/-2c7uHQUiPUvF34DV16HMw"},
    {"id": 7, "name": "郭砚宾", "gender": "男", "birth": "", "current_post": "县委常委、组织部长", "current_org": "中共乡宁县委员会", "source": "https://mp.weixin.qq.com/s/_4yyajG6ilWUzySfoIi8nQ"},
    {"id": 8, "name": "张晓丽", "gender": "女", "birth": "1985.06", "current_post": "县委常委、副县长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10943/2361.html"},
    {"id": 9, "name": "王晓磊", "gender": "男", "birth": "", "current_post": "县委常委、人武部长", "current_org": "乡宁县人民武装部", "source": "https://mp.weixin.qq.com/s/RRUnoUo3dUeCT0Oy5lOsZw"},
    {"id": 10, "name": "苏政锦", "gender": "男", "birth": "", "current_post": "县委常委（推测：纪委书记或统战部长）", "current_org": "中共乡宁县委员会", "source": "https://mp.weixin.qq.com/s/nGSzh4e9BQvJtQWB5U3lUQ"},
    {"id": 11, "name": "王嘉", "gender": "男", "birth": "", "current_post": "县委常委（推测：统战部长或县委办主任）", "current_org": "中共乡宁县委员会", "source": "https://mp.weixin.qq.com/s/ayfVaQRfM_P6PfqqlfQfGA"},
    {"id": 12, "name": "武红权", "gender": "男", "birth": "", "current_post": "乡宁示范区管委会主任", "current_org": "乡宁生态文化旅游示范区", "source": "https://mp.weixin.qq.com/s/9hplVdWXJWToJ9qSTQ4rRA"},
    {"id": 13, "name": "刘建平", "gender": "男", "birth": "", "current_post": "县人大常委会主任", "current_org": "乡宁县人大常委会", "source": "https://mp.weixin.qq.com/s/9hplVdWXJWToJ9qSTQ4rRA"},
    {"id": 14, "name": "高国荣", "gender": "男", "birth": "", "current_post": "县政协主席", "current_org": "乡宁县政协", "source": "https://mp.weixin.qq.com/s/_8GqrYeHetG5ZIIbmgLQyg"},
    {"id": 15, "name": "贺伟科", "gender": "男", "birth": "1974.12", "current_post": "副县长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10943/677.html"},
    {"id": 16, "name": "李军伟", "gender": "男", "birth": "1978.09", "current_post": "副县长、公安局长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10943/679.html"},
    {"id": 17, "name": "卫明", "gender": "男", "birth": "1980.12", "current_post": "副县长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10943/676.html"},
    {"id": 18, "name": "姬王鹏", "gender": "男", "birth": "1986.05", "current_post": "副县长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10943/681.html"},
    {"id": 19, "name": "邱肸靖", "gender": "男", "birth": "1984.10", "current_post": "副县长", "current_org": "乡宁县人民政府", "source": "http://www.xiangning.gov.cn/contents/10943/680.html"},
    {"id": 20, "name": "李乡民", "gender": "男", "birth": "", "current_post": "副县长", "current_org": "乡宁县人民政府", "source": "https://mp.weixin.qq.com/s/kgGbNAbilL0qzoFLAA9nBg"},
]

organizations = [
    {"id": 1, "name": "中共乡宁县委员会", "type": "党委", "level": "县级", "location": "乡宁县"},
    {"id": 2, "name": "乡宁县人民政府", "type": "政府", "level": "县级", "location": "乡宁县"},
    {"id": 3, "name": "乡宁县人大常委会", "type": "人大", "level": "县级", "location": "乡宁县"},
    {"id": 4, "name": "乡宁县政协", "type": "政协", "level": "县级", "location": "乡宁县"},
    {"id": 5, "name": "乡宁县人民武装部", "type": "党委", "level": "县级", "location": "乡宁县"},
    {"id": 6, "name": "乡宁生态文化旅游示范区", "type": "开发区", "level": "县级", "location": "乡宁县"},
    {"id": 7, "name": "乡宁县公安局", "type": "政府", "level": "科级", "location": "乡宁县"},
]

positions = [
    # Party committee
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "2026-06", "end_date": "", "rank": "副县级", "note": "新任"},
    {"person_id": 9, "org_id": 1, "title": "县委常委、人武部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 10, "org_id": 1, "title": "县委常委（推定：纪委书记/统战部长）", "start_date": "", "end_date": "", "rank": "副县级", "note": "推定"},
    {"person_id": 11, "org_id": 1, "title": "县委常委（推定：统战部长/县委办主任）", "start_date": "", "end_date": "", "rank": "副县级", "note": "推定"},
    # Government
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025-12", "end_date": "", "rank": "正县级", "note": "现任"},
    {"person_id": 4, "org_id": 2, "title": "副县长（常务）", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任，县委常委"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "2026-06", "end_date": "", "rank": "副县级", "note": "现任，县委常委"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 16, "org_id": 2, "title": "副县长、公安局长", "start_date": "2025-10", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "2021-05", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start_date": "2025-12", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 19, "org_id": 2, "title": "副县长", "start_date": "2023-12", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 20, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    # People's Congress
    {"person_id": 13, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    # CPPCC
    {"person_id": 14, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "现任"},
    # Armed Forces
    {"person_id": 9, "org_id": 5, "title": "人武部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任，县委常委"},
    # Others
    {"person_id": 12, "org_id": 6, "title": "示范区管委会主任", "start_date": "", "end_date": "", "rank": "副县级", "note": "现任"},
    {"person_id": 16, "org_id": 7, "title": "公安局长", "start_date": "2025-10", "end_date": "", "rank": "副县级", "note": "现任"},
]

relationships = [
    # 县委常委会核心关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与专职副书记", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与常委副县长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与政法委书记", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与宣传部长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记与组织部长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与常委副县长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "县委书记与人武部长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "县长与专职副书记", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    # 县政府班子关系
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "县长与副县长", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "县长与公安局长", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "县长与副县长", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "县长与副县长", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 19, "type": "上下级", "context": "县长与副县长", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 20, "type": "上下级", "context": "县长与副县长", "overlap_org": "乡宁县人民政府", "overlap_period": "现任"},
    # 人大政协
    {"person_a": 1, "person_b": 13, "type": "党政与人大", "context": "县委书记与人大主任", "overlap_org": "乡宁县", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 14, "type": "党政与政协", "context": "县委书记与政协主席", "overlap_org": "乡宁县", "overlap_period": "现任"},
    # 常委班子成员之间
    {"person_a": 4, "person_b": 8, "type": "同级", "context": "两位常委副县长", "overlap_org": "乡宁县人民政府", "overlap_period": "2026.06起"},
    {"person_a": 5, "person_b": 6, "type": "常委共事", "context": "政法委书记与宣传部长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
    {"person_a": 6, "person_b": 7, "type": "常委共事", "context": "宣传部长与组织部长", "overlap_org": "中共乡宁县委员会", "overlap_period": "现任"},
]

if __name__ == "__main__":
    run_build(
        slug="乡宁县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "xiangning_network.db",
        gexf_path=GRAPH_DIR / "xiangning_network.gexf",
        overwrite=True,
    )
    print("Done! Database and GEXF files created.")
