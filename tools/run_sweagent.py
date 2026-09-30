"""SWE-agent を fixture タスク（T1–T6 等）で実行するランナー。

fixture/ を git repo 化して runs/sweagent/<TASK>/run<N>/repo に置き、
tasks/<TASK>-*/prompt.txt を problem statement として `sweagent run` を実行する。
実行条件は runs/sweagent/T6/run1/out/*/config.yaml で確定したものを踏襲
（default.yaml + gemini/gemini-3.5-flash-lite + local repo + docker）。

usage:
  python tools/run_sweagent.py T1          # 単一タスク
  python tools/run_sweagent.py T1 T2 T3    # 複数タスク順次

前提:
  - .tools/SWE-agent/.venv に sweagent が editable install 済み
  - .secrets/gemini-key.txt に Gemini API キー（GEMINI_API_KEY として子プロセスへ渡す）
  - Docker が起動していること

既知の問題（plan.md §7 参照）:
  - .tools/SWE-agent を autocrlf 付きで clone すると tools/ 以下の
    シェルスクリプトが CRLF 化し、コンテナ内で submit 時の
    _state_anthropic が `env: 'python3\\r'` で失敗し続ける。
    実行前に tools/ のスクリプトを LF 変換すること。
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
SWE = BENCH / ".tools" / "SWE-agent"
VENV_PY = SWE / ".venv" / "Scripts" / "python.exe"
KEY_FILE = BENCH / ".secrets" / "gemini-key.txt"
FIXTURE = BENCH / "fixture"
RUNS = BENCH / "runs" / "sweagent"

MODEL = "gemini/gemini-3.5-flash-lite"


def find_prompt(task: str) -> Path:
    matches = sorted((BENCH / "tasks").glob(f"{task}-*/prompt.txt"))
    if not matches:
        sys.exit(f"prompt not found: tasks/{task}-*/prompt.txt")
    return matches[0]


def prep_repo(dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(FIXTURE, dst, ignore=shutil.ignore_patterns("__pycache__"))
    subprocess.run(["git", "init", "-q"], cwd=dst, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dst, check=True)
    subprocess.run(
        ["git", "-c", "user.email=bench@local", "-c", "user.name=bench",
         "commit", "-qm", "fixture snapshot"],
        cwd=dst, check=True,
    )


def run_task(task: str, run_no: int = 1) -> int:
    prompt = find_prompt(task)
    run_dir = RUNS / task / f"run{run_no}"
    repo = run_dir / "repo"
    out = run_dir / "out"
    prep_repo(repo)
    out.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env["GEMINI_API_KEY"] = KEY_FILE.read_text(encoding="utf-8").strip()
    env["PYTHONUTF8"] = "1"

    cmd = [
        str(VENV_PY), "-m", "sweagent", "run",
        "--config", "config/default.yaml",
        "--env.repo.type=local",
        f"--env.repo.path={repo}",
        "--problem_statement.type=text_file",
        f"--problem_statement.path={prompt}",
        f"--output_dir={out}",
        f"--agent.model.name={MODEL}",
        "--agent.model.temperature=0",
        "--agent.model.top_p=1.0",
        "--agent.model.per_instance_cost_limit=3.0",
    ]
    print(f"[{task}] start: repo={repo} out={out}", flush=True)
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=SWE, env=env)
    elapsed = int(time.time() - t0)
    print(f"[{task}] done: exit={proc.returncode} {elapsed}s", flush=True)
    return proc.returncode


def main() -> None:
    tasks = sys.argv[1:] or sys.exit("usage: python tools/run_sweagent.py T1 [T2 ...]")
    for t in tasks:
        run_task(t)


if __name__ == "__main__":
    main()
