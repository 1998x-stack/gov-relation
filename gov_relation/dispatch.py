"""Generate queue-driven investigation dispatch prompts."""

from __future__ import annotations

from dataclasses import dataclass

from .slugs import artifact_paths
from .todo import TodoItem, item_summary


@dataclass(frozen=True)
class DispatchPlan:
    task: dict
    model_intent: str
    prompt: str
    suggested_command: str


def build_dispatch_prompt(item: TodoItem, model_intent: str = "standard") -> str:
    task = item_summary(item)
    paths = artifact_paths(task["region"])
    targets = " & ".join(task["target_roles"])
    parent_city = task["parent_city"] or ""
    return f"""Use the china-gov-network skill at .agents/skills/china-gov-network.

Task:
- task_id: {task["task_id"]}
- province: {task["province"]}
- parent_city: {parent_city}
- region: {task["region"]}
- level: {task["level"]}
- targets: {targets}
- model_intent: {model_intent}

Expected artifact paths:
- staging_dir: data/tmp/{task["task_id"]}/
- build_script: data/tmp/{task["task_id"]}/{paths["build_script"]}
- database: data/tmp/{task["task_id"]}/{paths["db_output"].split("/")[-1]}
- gexf: data/tmp/{task["task_id"]}/{paths["gexf_output"].split("/")[-1]}
- person_json_pattern: data/tmp/{task["task_id"]}/YYYYMMDD-{task["province"]}-{parent_city or task["region"]}-{{job}}-{{name}}.json

Canonical destination after validation:
- build_script: {paths["build_script"]}
- database: {paths["db_output"]}
- gexf: {paths["gexf_output"]}
- person_json_dir: data/persons/

Required workflow:
1. Run Phase 0 repository preflight.
2. Read relevant references from .agents/skills/china-gov-network/references:
   - investigation_stages.md
   - subagent_dispatch.md
   - person_graph_json.md
   - gexf_pattern.md when writing graph output
3. Research current officeholders, leadership roster, biographies, predecessor/successor moves, relationship evidence, governance/professional profile, and open gaps.
4. Write all newly generated artifacts into the staging directory first. Do not write new build scripts into repo root directly.
5. Validate with py_compile, script execution, json.tool for person JSON, and scripts/process_tmp.py data/tmp/{task["task_id"]}.
6. Promote with scripts/process_tmp.py data/tmp/{task["task_id"]} --apply only after the dry run is clean.
7. Run scripts/inventory.py after promotion.
8. Do not mark the TODO item done unless validation passes. After validation and promotion pass, run:
   python3 scripts/todo_queue.py done --task-id {task["task_id"]} --worker-id <YOUR_WORKER_ID>
"""


def build_dispatch_plan(item: TodoItem, model_intent: str = "standard") -> DispatchPlan:
    task = item_summary(item)
    prompt = build_dispatch_prompt(item, model_intent=model_intent)
    suggested_command = "opencode run --agent build --model <MODEL> '<PROMPT_FROM_STDOUT>'"
    return DispatchPlan(task=task, model_intent=model_intent, prompt=prompt, suggested_command=suggested_command)
