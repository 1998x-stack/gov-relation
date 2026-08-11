# v3 前序 Phase 优化清单(SubAgentReview 后)

- **日期:** 2026-08-11
- **来源:** 三份审查报告 `docs/superpowers/reviews/2026-08-11-review-*.md`(Phase 1 CHANGES-REQUESTED / Phase 2 CHANGES-REQUESTED / Phase 3 APPROVED)
- **原则:** 先文档同步 → 再小步代码修复 → 提交与决策项逐项确认 → 最后进 Phase 4

---

## A. 文档/规范同步(零风险,已执行)

- [x] **spec §11 Phase 2 废弃标注** — `schema.py` 升 v3 DDL、`ADDITIVE_SCHEMA_UPGRADES` 纳入 2.1.0 两处旧方案已划除并指向 Phase 2 计划 Task 1 废弃声明(factory 持有 v3 DDL、upgrades 保持空集)。
- [x] **spec §4.5 `gold_current_positions` 语义同步** — 注明已实现视图读 `positions.is_current=1`(person_statuses 保留为实体表,不再作视图数据源)。
- [x] **spec §9.2 `BuildScriptFactory.generate()` 签名同步** — 已实现为 keyword-only `(slug, province_name, …)`、经 `runner.run_build(backend="v3")` 执行、`parents[2]` 定位仓库根。
- [x] **spec 顶部修订注记** — 声明行为以实现与 Phase 计划为准。
- [x] **Phase 1 清单过期数字修正** — `tests/test_factory/` 25→32 个、全量 222→241 passed(注记基线差异)。

## B. 功能/健壮性修复(小步代码改动,待执行)

- [ ] **Phase 1 F4 修复** — 生成脚本硬编码 `parents[2]`,location-agnostic 声明不成立:给 `build_factory` 增加向上搜索 `gov_relation/` 定位仓库根的兜底;或降低 plan 声明。推荐实现 + 保留现有深度假设。
- [ ] **Phase 3 人名兜底解析守卫** — 对齐 plan 参考实现的 `isdigit()`/长度守卫,非 8 位日期前缀不再一律截 3 段;改后必须复跑 dry-run 确认 unmatched=0 结果不变(或只变好)。
- [ ] **gold_current_positions 补一个视图语义测试**(当前无测试覆盖)。

## C. 仓库健康(需老板拍板)

- [ ] **Phase 1-2 补提交** — factory/、identity.py、paths.py、tests/test_factory/、external_data_merge json(Phase 1);upgrade_schema_v2_to_v3.py + govdb.py + platform/schema.py 及门禁测试(Phase 2);Phase 3 测试文件。建议 3 个 commit,plan 的 Commit 步骤补勾。docs/reports 海量 untracked 为日常流水线产物,不纳入。
- [ ] **data/provinces/ 处置** — 11,214 个产物 / 158MB 未跟踪也未 gitignore。选项:(a) 按项目惯例(commit 7f2a7bd59 已 untrack runtime data)加入 .gitignore(推荐);(b) 全部入库(158MB)。
- [ ] **分歧分支处置** — `worktree-v3-refactor`(.claude/worktrees/v3-refactor,4 commits,旧实现)非 main 祖先,内容已被工作树新版取代;确认后删除分支 + 移除 worktree。
- [ ] **Phase 2 备份缺件** — `.pre-v3.bak` 未落盘(库已迁移,无法补历史备份);建议在 plan 完成记录中注明"备份未落盘"以闭合审计,后续 DB 迁移强制先备份。

## C2. 已顺手确认的事项

- [x] `.gitignore` 现有 `*.bak` 追加(他线改动)— 保留不冲突。
- [x] docs/reports 海量新 HTML = 日常研究流水线产物,非 Phase 遗留,不动。

---

**完成标准:** A 全过 + B 全部实现且全量测试 241 通过、dry-run 门禁不变 + C 逐项确认落地 → 开 Phase 4。