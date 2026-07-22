"""Read-only web helpers for local API and static site data."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .inventory import collect_inventory
from .log import get_logger
from .paths import DATABASE_DIR, DOCS_DIR, GRAPH_DIR, PERSONS_DIR, REPORT_DIR, REPO_ROOT

logger = get_logger(__name__)


def list_databases() -> list[dict]:
    rows = []
    for path in sorted(DATABASE_DIR.glob("*.db")):
        rows.append({"name": path.name, "stem": path.stem, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size})
    return rows


def list_graphs() -> list[dict]:
    rows = []
    for path in sorted(GRAPH_DIR.glob("*.gexf")):
        rows.append({"name": path.name, "stem": path.stem, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size})
    return rows


def list_reports() -> list[dict]:
    rows = []
    for path in sorted(REPORT_DIR.glob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            rows.append({"name": path.name, "path": str(path.relative_to(REPO_ROOT)), "type": path.suffix.lstrip("."), "size": path.stat().st_size})
    return rows


def list_person_profiles() -> list[dict]:
    rows = []
    if not PERSONS_DIR.exists():
        return rows
    for path in sorted(PERSONS_DIR.glob("*.json")):
        record = {"name": path.name, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            identity = data.get("identity", {})
            scope = data.get("investigation_scope", {})
            record.update(
                {
                    "person": identity.get("name", ""),
                    "job": scope.get("job", ""),
                    "province": scope.get("province", ""),
                    "city": scope.get("city", ""),
                    "current_post": data.get("current_status", {}).get("current_post", ""),
                }
            )
        except Exception as exc:  # keep inventory robust for partially written files
            record["error"] = str(exc)
        rows.append(record)
    return rows


def database_summary(name: str) -> dict:
    path = DATABASE_DIR / name
    if not path.exists() or path.suffix != ".db":
        raise FileNotFoundError(name)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        cur = conn.cursor()
        counts = {}
        for table in ["persons", "organizations", "positions", "relationships"]:
            try:
                counts[table] = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except sqlite3.Error:
                counts[table] = None
        return {"name": name, "path": str(path.relative_to(REPO_ROOT)), "counts": counts}
    finally:
        conn.close()


def database_rows(name: str, table: str, limit: int = 500) -> list[dict]:
    if table not in {"persons", "organizations", "positions", "relationships"}:
        raise ValueError(table)
    path = DATABASE_DIR / name
    if not path.exists() or path.suffix != ".db":
        raise FileNotFoundError(name)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table} LIMIT ?", (limit,))]
    finally:
        conn.close()


def static_payload() -> dict:
    inv = collect_inventory()
    dbs = list_databases()
    summaries = []
    for db in dbs:
        try:
            summaries.append(database_summary(db["name"]))
        except Exception as exc:
            summaries.append({"name": db["name"], "error": str(exc)})
    return {
        "inventory": asdict(inv),
        "databases": dbs,
        "database_summaries": summaries,
        "graphs": list_graphs(),
        "reports": list_reports(),
        "person_profiles": list_person_profiles(),
    }


def write_static_site_data(output_dir: Path = DOCS_DIR / "assets" / "data") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = static_payload()
    for key, value in payload.items():
        (output_dir / f"{key}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class GovRelationHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory or str(DOCS_DIR), **kwargs)

    def _send_json(self, data: object, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        try:
            if path == "/api/inventory":
                return self._send_json(asdict(collect_inventory()))
            if path == "/api/databases":
                return self._send_json(list_databases())
            if path.startswith("/api/database/"):
                parts = path.split("/")
                name = parts[3]
                if len(parts) == 5 and parts[4] in {"persons", "organizations", "positions", "relationships"}:
                    return self._send_json(database_rows(name, parts[4]))
                return self._send_json(database_summary(name))
            if path == "/api/graphs":
                return self._send_json(list_graphs())
            if path == "/api/reports":
                return self._send_json(list_reports())
            if path == "/api/person-profiles":
                return self._send_json(list_person_profiles())
        except Exception as exc:
            return self._send_json({"error": str(exc)}, status=404)
        return super().do_GET()


def serve(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), GovRelationHandler)
    return server

