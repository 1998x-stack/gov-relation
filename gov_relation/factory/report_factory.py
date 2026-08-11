"""Generate concise Markdown investigation reports."""

from __future__ import annotations

import sqlite3
from datetime import date


class ReportFactory:
    """Render report content from aggregate regional statistics."""

    def build(self, slug: str, stats: dict[str, int]) -> str:
        return f"""# {slug} 领导班子调查

**生成日期:** {date.today().isoformat()}

## 数据概览

| 指标 | 数量 |
|------|------|
| 人员 | {stats.get('persons', 0)} |
| 组织 | {stats.get('organizations', 0)} |
| 任职记录 | {stats.get('positions', 0)} |
| 关系 | {stats.get('relationships', 0)} |
| 来源 | {stats.get('sources', 0)} |

## 现任领导

<!-- TODO: fill in from confirmed current positions -->

## 关系网络摘要

<!-- TODO: summarize evidence-backed relationships -->

## 开放问题

<!-- TODO: document gaps and uncertainties -->
"""

    def build_from_conn(self, conn: sqlite3.Connection, slug: str) -> str:
        stats: dict[str, int] = {}
        for table in (
            "persons", "organizations", "positions", "relationships", "sources"
        ):
            stats[table] = conn.execute(
                f"SELECT COUNT(*) FROM [{table}]"
            ).fetchone()[0]
        return self.build(slug, stats)
