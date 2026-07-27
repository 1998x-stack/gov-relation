# 统一中央数据仓库设计方案

**日期**: 2026-07-27
**状态**: 设计稿 v1
**目标**: 将所有现有及持续新增的政府人员关系数据，统一到按省份分区的中央 SQLite 数据仓库中

---

## 1. 核心决策

| 决策 | 选择 |
|------|------|
| 目标 | 全国统一大库，所有地区数据汇总到同一组表 |
| 迁移方式 | 一次性全量迁移已有 ~1668 个独立 DB |
| ID 策略 | Content-hash（SHA256）作为主键，解决冲突 |
| 合并规则 | 姓名 + birth → 自动合并为同一人 |
| 存储引擎 | SQLite WAL 模式 + 按省份分区 |
| 持续增量 | 新 build 脚本通过 `CentralWriter` API 直接写入中央库 |

---

## 2. 分区结构

```
data/central/
  registry.db                         ← 元数据：省份分区列表、迁移状态、数据版本
  henan.db                            ← 河南省全量数据 (WAL 模式)
  hubei.db                            ← 湖北省全量数据
  guangdong.db                        ← 广东省全量数据
  ...每个省份一个
  unknown.db                          ← 暂未确定省份归属的数据
  cross_province.db                   ← 跨省关联索引（同一人的跨省任职轨迹）
```

每个省份 DB 内**不包含冗余的省份列**——分区本身就是隐式的省份属性。跨省查询通过 Python API 在多个 DB 上使用 `ATTACH DATABASE` 实现。

---

## 3. 表结构设计

### 3.1 `persons` 表

```sql
CREATE TABLE persons (
    id_hash TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    name_normalized TEXT NOT NULL,
    gender TEXT DEFAULT '',
    ethnicity TEXT DEFAULT '',
    birth TEXT DEFAULT '',
    birthplace TEXT DEFAULT '',
    education TEXT DEFAULT '',
    party_join TEXT DEFAULT '',
    work_start TEXT DEFAULT '',
    aliases TEXT DEFAULT '[]',
    source_json TEXT DEFAULT '{}',
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_persons_name ON persons(name);
CREATE INDEX idx_persons_birth ON persons(birth);
```

### 3.2 `organizations` 表

```sql
CREATE TABLE organizations (
    id_hash TEXT PRIMARY KEY,
    fqn TEXT NOT NULL,
    local_name TEXT NOT NULL,
    org_type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent_fqn TEXT DEFAULT '',
    location TEXT DEFAULT '',
    province TEXT NOT NULL
);

CREATE INDEX idx_orgs_fqn ON organizations(fqn);
CREATE INDEX idx_orgs_province ON organizations(province);
```

### 3.3 `positions` 表

```sql
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_hash TEXT NOT NULL,
    org_hash TEXT NOT NULL,
    title TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    rank TEXT DEFAULT '',
    category TEXT DEFAULT '',
    note TEXT DEFAULT '',
    province TEXT NOT NULL,
    source TEXT DEFAULT '',
    FOREIGN KEY (person_hash) REFERENCES persons(id_hash),
    FOREIGN KEY (org_hash) REFERENCES organizations(id_hash)
);

CREATE INDEX idx_positions_person ON positions(person_hash);
CREATE INDEX idx_positions_org ON positions(org_hash);
CREATE INDEX idx_positions_province ON positions(province);
```

### 3.4 `relationships` 表

```sql
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a_hash TEXT NOT NULL,
    person_b_hash TEXT NOT NULL,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org_hash TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    province TEXT NOT NULL,
    source TEXT DEFAULT '',
    FOREIGN KEY (person_a_hash) REFERENCES persons(id_hash),
    FOREIGN KEY (person_b_hash) REFERENCES persons(id_hash),
    FOREIGN KEY (overlap_org_hash) REFERENCES organizations(id_hash)
);
```

### 3.5 `registry.db` — 元数据表

```sql
CREATE TABLE region_registry (
    province TEXT PRIMARY KEY,
    db_path TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    person_count INTEGER DEFAULT 0,
    org_count INTEGER DEFAULT 0,
    position_count INTEGER DEFAULT 0,
    relation_count INTEGER DEFAULT 0,
    migrated_at TEXT,
    last_updated TEXT
);

CREATE TABLE migration_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_db TEXT NOT NULL,
    slug TEXT NOT NULL,
    province TEXT NOT NULL,
    persons_imported INTEGER DEFAULT 0,
    orgs_imported INTEGER DEFAULT 0,
    positions_imported INTEGER DEFAULT 0,
    rels_imported INTEGER DEFAULT 0,
    merge_conflicts INTEGER DEFAULT 0,
    migrated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE merge_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conflict_type TEXT NOT NULL,
    left_data TEXT,
    right_data TEXT,
    resolution TEXT DEFAULT 'pending',
    resolved_by TEXT DEFAULT '',
    resolved_at TEXT
);
```

---

## 4. 哈希与冲突策略

### 4.1 id_hash 生成规则

| 实体 | 哈希输入 | 示例 |
|------|----------|------|
| person | `SHA256(normalize(name) + "\|" + normalize(birth))[:16]` | `SHA256("詹鹏\|1977-01")[:16]` |
| org | `SHA256(province + "\|" + normalize(fqn))[:16]` | `SHA256("河南省\|周口市人民政府")[:16]` |

`normalize()` 做：统一全角/半角、去除多余空格、繁体转简体（对中文名）。

`birth` 为空时用空字符串替代 hash 输入，以确保姓名相同但 birth 缺失的数据仍可选择性地自动合并。

### 4.2 冲突分层

| 冲突情况 | 处理策略 |
|----------|----------|
| hash 相同 + 内容完全一致 | 跳过（重复数据） |
| hash 相同 + 内容有差异 | UPSERT 合并字段（字段级覆盖或保留最新） |
| hash 不同但 name 相同 + birth 不同 | 写入 `merge_conflicts`，标记 `pending`，等待人工判定 |
| hash 不同但 name 相同 + birth 缺失 | 后台 fuzzy pass 尝试推测合并，无法确定的也标记 pending |

---

## 5. 一次性迁移脚本

脚本 `scripts/migrate_to_central.py` 流程：

```
1. 遍历 data/database/*_network.db
   2. 步骤 A：slug 提取
      - 文件名 "周口市_network.db" → slug = "周口市"
      - 读取 TODO.json 或 slug 映射表 → 确定省份归属
   4. 步骤 B：数据抽取
      - 读取 persons → 每条记录计算 id_hash → UPSERT 到目标省 DB
      - 读取 organizations → 每条记录生成 fqn + 计算 hash → UPSERT
      - 读取 positions → 查询 person/org 的 hash → INSERT
      - 读取 relationships → 查询 person_a/b 的 hash → INSERT
   5. 步骤 C：审计记录
      - 写入 migration_audit（记录行数）
      - 如有合并冲突，写入 merge_conflicts
2. 汇总报告：
   - 处理了多少个 DB
   - 导入了多少行
   - 产生了多少冲突
   - 哪些 DB 无法确定省份
```

---

## 6. 新数据写入管道

改造 `gov_relation/runner.py` 和 `gov_relation/schema.py`，新增：

### `gov_relation/central.py` 模块

```python
class Central:
    """Writes data to the partitioned central registry."""

    def __init__(self, province: str):
        self.province = province
        self.conn = connect_province_db(province)

    def merge_person(self, person: dict) -> str:
        # 计算 id_hash → UPSERT
        pass

    def after_persons(self) -> dict[str, str]:
        # 将人员写入 person JSON 目录（可选）
        pass

    def merge_organization(self, org: dict) -> str:
        # 计算 id_hash → UPSERT
        pass

    def insert_position(self, position: dict):
        # INSERT 引用已存在的 person_hash 和 org_hash
        pass

    def insert_relationship(self, rel: dict):
        pass

    def close(self):
        self.conn.close()
```

### `gov_relation/runner.py` 新增入口

```python
def run_build(
    *, slug, persons, organizations, positions, relationships,
    db_path, gexf_path, central: Central | None = None
) -> None:
    # 1. 写地区 DB（向后兼容）
    run_local(...)
    # 2. 写中央库
    if central:
        central.merge_persons(persons)
        central.merge_organizations(organizations)
        central.insert_positions(positions)
        central.insert_relationships(relationships)
```

build 脚本只需额外传入 `central=Central(province=detect_province(slug))`，对现有脚本改动最小。

---

## 7. 路径与配置变更

### `gov_relation/paths.py` 新增

```python
CENTRAL_DIR = DATA_DIR / "central"
REGISTRY_DB = CENTRAL_DIR / "registry.db"
PROVINCE_DB_DIR = CENTRAL_DIR / "provincial"
```

### `gov_relation/schema.py` 新增

```python
def create_central_schema(conn: sqlite3.Connection) -> None:
    """创建中央库的所有表（persons/orgs/positions/relationships + 元数据表）"""
```

---

## 8. 与现有系统的兼容性

| 现有系统 | 兼容方式 |
|----------|----------|
| `build_*_data.py` 脚本 | 无需修改，熟悉的脚本可继续使用（写入地区 DB） |
| `run_build()` 函数 | 扩展签名（新增可选 `central` 参数） |
| `data/database/*.db` | 保留，只读时可用 |
| `data/graph/*.gexf` | 由地区 DB 构建，不受影响 |
| Web 后端（serve_app.py） | 优先读取中央库，fallback 到地区 DB |
| `inventory.py` | 新增中央库盘点 |

---

## 9. 设计原则

- **向下兼容**：所有现存文件和接口保持不变
- **增量优先**：一次迁移脚本执行后，后续新增数据通过 build 管道的 API 自然流入
- **分区隔离**：省份级分区避免了一整个大文件写锁争用，WAL 模式确保多个 worker 可以同时写入不同省份
- **可审计**：所有迁移操作记录到 registry.db 的审计表；所有合并冲突需要人工判定的记录到 merge_conflicts