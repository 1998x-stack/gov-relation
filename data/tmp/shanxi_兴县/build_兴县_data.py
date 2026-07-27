#!/usr/bin/env python3
"""Build 兴县 leadership network database and GEXF graph.

Current leadership as of 2026-07-26:
- 梁文壮: 县委书记, 县长 (both positions)
  Source: Baidu Baike 兴县 political section (as of 2024年8月)

Note: 梁文壮 serves as both Party Secretary and County Mayor.
This is an unusual arrangement suggesting a temporary leadership situation
or combined appointment.

Research limitations (2026-07-26):
- All Chinese government websites (www.xingxian.gov.cn) timeout
- Baidu Baike returns 403 for individual person pages
- Exa search rate-limited
- Jina Reader times out
- No Playwright browser available
- Bing/Google/360 all block automated access
- GitHub code search found no references

Person biography details (birth year, education, career timeline, gender,
birthplace, party_join) are all open_gaps due to complete web research blockade.

Artifact conventions:
- Build script: build_兴县_data.py -> scripts/build/build_兴县_data.py
- Database: data/database/兴县_network.db
- GEXF: data/graph/兴县_network.gexf
"""

from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # uses sqlite3
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "兴县_network.db"
GEXF_PATH = GRAPH_DIR / "兴县_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "梁文壮",
        "gender": "",          # unknown - research blocked
        "birth": "",           # unknown - research blocked
        "current_post": "县委书记、县长",
        "current_org": "中共兴县委员会 / 兴县人民政府",
        "source": "https://baike.baidu.com/item/兴县",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共兴县委员会",
        "type": "党委",
        "level": "县级",
        "location": "兴县",
    },
    {
        "id": 2,
        "name": "兴县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "兴县",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委书记",
        "start_date": "",
        "end_date": "",
        "rank": "正县级",
        "note": "现任（Baike Baidu 政治栏目截至2024年8月）",
    },
    {
        "person_id": 1,
        "org_id": 2,
        "title": "县长",
        "start_date": "",
        "end_date": "",
        "rank": "正县级",
        "note": "现任，一肩挑兼任",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 1,
        "type": "党政一肩挑",
        "context": "梁文壮同时担任兴县县委书记和县长",
        "overlap_org": "兴县",
        "overlap_period": "截至2024年8月",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="兴县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )