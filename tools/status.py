"""bench/ の計測・記入状況を集計して STATUS.md を生成する。
results/*.json + reviews/*.json + runs/ の成果物を走査し、
タスク実施状況・レビュー記入状況・成果物との乖離を一覧化する。

usage: python tools/status.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
OUT = BENCH / "STATUS.md"

REVIEWERS = ["ChatGPT", "Gemini", "Claude", "Devin (SWE-2)"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_mark(run) -> str:
    if run.get("success") is True or run.get("success") == "○":
        return "✓"
    if run.get("success") is False or run.get("success") == "×":
        return "✗"
    if run.get("success") in ("—", "-"):
        return "—"
    return "?"


def fill_ratio(d: dict) -> tuple[int, int]:
    vals = [v for v in d.values()]
    done = sum(1 for v in vals if v not in ("?", None))
    return done, len(vals)


def fill_mark(done: int, total: int) -> str:
    if total == 0:
        return "—"
    if done == total:
        return "✓"
    if done == 0:
        return "?"
    return f"△{done}/{total}"


def cell_marks(runs: list) -> str:
    """同一タスクに複数runがある場合をまとめて表示。"""
    if not runs:
        return "—"
    marks = [run_mark(r) for r in runs]
    if len(runs) == 1:
        return marks[0]
    ok = marks.count("✓")
    if ok:
        return f"✓({ok}/{len(runs)})"
    ng = marks.count("✗")
    if ng:
        return f"✗({ng}/{len(runs)})"
    return "?"


def main() -> None:
    data = load_json(BENCH / "data" / "editors.json")
    editors = data["editors"]
    categories = data["categories"]
    models = data.get("models", {})

    results_map = {p.stem: load_json(p) for p in sorted((BENCH / "results").glob("*.json"))}
    reviews_map = {p.stem: load_json(p) for p in sorted((BENCH / "reviews").glob("*.json"))}

    # 全カテゴリに出現するタスクIDを収集
    cat_tasks: dict[str, list[str]] = {}
    for res in results_map.values():
        for r in res.get("runs", []):
            cat_tasks.setdefault(r["category"], [])
            if r["task"] not in cat_tasks[r["category"]]:
                cat_tasks[r["category"]].append(r["task"])
    for t in cat_tasks.values():
        t.sort()

    # runs/ 成果物の収集: runs/<editor>/<task>/runN
    artifacts: dict[tuple[str, str], list[str]] = {}
    runs_root = BENCH / "runs"
    if runs_root.is_dir():
        for ed_dir in sorted(runs_root.iterdir()):
            if not ed_dir.is_dir():
                continue
            for task_dir in sorted(ed_dir.iterdir()):
                if not task_dir.is_dir():
                    continue
                run_dirs = [d.name for d in task_dir.iterdir() if d.is_dir()]
                artifacts[(ed_dir.name, task_dir.name)] = run_dirs

    lines: list[str] = []
    w = lines.append
    w("# ベンチマーク実施状況")
    w("")
    w(f"生成: {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M %z')} — `tools/status.py` により自動生成")
    w("")
    w("再生成: `python tools/status.py`（`results/`・`reviews/`・`runs/` 更新後に実行）")
    w("")
    w("記号: `✓` 成功 / `✗` 失敗 / `?` 枠あり・未計測 / `—` 枠なしまたは省略（計測不可）。")
    w("同一タスク複数runは `✓(n/m)` の形式。成果物ありだが結果未記録は「乖離」節を参照。")
    w("")

    # ---- サマリ ----
    w("## サマリ")
    w("")
    w("| カテゴリ | モデル | ✓ | ✗ | ? | — |")
    w("|---|---|---|---|---|---|")
    for cat_id in cat_tasks:
        ok = ng = unk = skip = 0
        for e in editors:
            runs = results_map.get(e["id"], {}).get("runs", [])
            for r in runs:
                if r["category"] != cat_id:
                    continue
                m = run_mark(r)
                ok += m == "✓"
                ng += m == "✗"
                unk += m == "?"
                skip += m == "—"
        w(f"| {categories.get(cat_id, cat_id)} | {models.get(cat_id, '—')} | {ok} | {ng} | {unk} | {skip} |")
    w("")

    # ---- タスク行列（カテゴリ別）----
    w("## 定量ベンチ 実施状況（ツール×タスク）")
    w("")
    for cat_id, cat_label in categories.items():
        tasks = cat_tasks.get(cat_id, [])
        if not tasks:
            continue
        members = [
            e for e in editors
            if any(r["category"] == cat_id for r in results_map.get(e["id"], {}).get("runs", []))
        ]
        model = models.get(cat_id, "")
        w(f"### {cat_label}" + (f"（{model}）" if model else ""))
        w("")
        w("| ツール | " + " | ".join(tasks) + " |")
        w("|" + "---|" * (len(tasks) + 1))
        for e in members:
            runs = results_map.get(e["id"], {}).get("runs", [])
            by_task: dict[str, list] = {}
            for r in runs:
                if r["category"] == cat_id:
                    by_task.setdefault(r["task"], []).append(r)
            cells = [cell_marks(by_task.get(t, [])) for t in tasks]
            w(f"| {e['name']} | " + " | ".join(cells) + " |")
        w("")

    # ---- レビュー記入状況 ----
    w("## 定性評価・レビュー記入状況")
    w("")
    w("| ツール | 機能マトリクス | 導入の容易さ | " + " | ".join(REVIEWERS) + " |")
    w("|" + "---|" * (len(REVIEWERS) + 3))
    for e in editors:
        rv = reviews_map.get(e["id"], {})
        matrix_done, matrix_total = fill_ratio(rv.get("matrix", {}))
        inst_done, inst_total = fill_ratio(rv.get("install", {}))
        rev_map = {r["reviewer"]: r for r in rv.get("usability_reviews", [])}
        rev_cells = []
        for name in REVIEWERS:
            r = rev_map.get(name)
            if not r:
                rev_cells.append("—")
                continue
            scores = r.get("scores", {})
            done, total = fill_ratio({**scores, "comment": r.get("comment", "?")})
            rev_cells.append(fill_mark(done, total))
        w(f"| {e['name']} | {fill_mark(matrix_done, matrix_total)} ({matrix_done}/{matrix_total})"
          f" | {fill_mark(inst_done, inst_total)} ({inst_done}/{inst_total})"
          f" | " + " | ".join(rev_cells) + " |")
    w("")

    # ---- runs/ 成果物との照合 ----
    w("## runs/ 成果物と results/ の照合")
    w("")
    missing_in_results = []
    missing_artifacts = []
    for (ed, task), run_dirs in sorted(artifacts.items()):
        res = results_map.get(ed, {})
        task_runs = [r for r in res.get("runs", []) if r["task"] == task]
        if not task_runs:
            missing_in_results.append(f"- `runs/{ed}/{task}/` ({len(run_dirs)} run) — results に行なし")
        elif all(run_mark(r) == "?" for r in task_runs):
            missing_in_results.append(f"- `runs/{ed}/{task}/` ({len(run_dirs)} run) — results は未計測のまま")
    for ed, res in results_map.items():
        for r in res.get("runs", []):
            if run_mark(r) != "✓":
                continue
            diff = str(r.get("diff_url", ""))
            if diff in ("?", "None", ""):
                missing_artifacts.append(f"- {ed} {r['task']} run{r['run']}: 成功だが diff_url 未採取")
            elif diff.startswith("runs/") and not (BENCH / diff).is_dir():
                missing_artifacts.append(f"- {ed} {r['task']} run{r['run']}: diff_url `{diff}` が存在しない")
    if missing_in_results:
        w("### 成果物あり・results 未記録（記録漏れの可能性）")
        w("")
        w("\n".join(missing_in_results))
        w("")
    if missing_artifacts:
        w("### results に成功記録・成果物なし")
        w("")
        w("\n".join(missing_artifacts))
        w("")
    if not missing_in_results and not missing_artifacts:
        w("乖離なし。")
        w("")

    # ---- 残作業 ----
    w("## 残作業の目安")
    w("")
    remaining = []
    for e in editors:
        runs = results_map.get(e["id"], {}).get("runs", [])
        unk = sum(1 for r in runs if run_mark(r) == "?")
        if unk:
            remaining.append(f"- {e['name']}: 未計測 {unk} 枠")
    w("\n".join(remaining) if remaining else "- 全枠計測済み")
    w("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("generated:", OUT)


if __name__ == "__main__":
    main()
