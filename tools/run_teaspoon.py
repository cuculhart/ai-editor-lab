"""Teaspoon IDE (Electron) を Playwright で駆動してベンチタスクを実行する。

- パッケージ済み exe (teaspoon-ide/out/Teaspoon-win32-x64/Teaspoon.exe) を起動
- 作業フォルダを CLI 引数で渡してプロジェクトを開く
- localStorage で Ollama プロバイダを事前設定して reload
- プロンプト送信 → 承認ダイアログを逐次 approve（クリック回数 = 介入数）
- send ボタン再有効化＝生成完了、または 900 秒タイムアウトで終了
- 結果: agent.log（チャットダンプ）+ screenshot.png を run ディレクトリに保存

usage:
  python tools/run_teaspoon.py T1 [T2 ...]

前提:
  - Ollama 起動済み・qwen3.5:4b pull 済み
  - teaspoon-ide が package 済み（npm run package）
  - python -m playwright install 済み（Electron 自動化はブラウザDL不要）

記録上の注意:
  - 承認ダイアログは仕様上必須（auto-approve なし）なので approve クリックは
    全て「介入」としてカウントする（L1–L3 の記録と同じ基準）
"""
import http.client
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BENCH = Path(__file__).resolve().parents[1]
TEASPOON_EXE = (
    BENCH.parent / "teaspoon-ide" / "out" / "Teaspoon-win32-x64" / "Teaspoon.exe"
)
FIXTURE = BENCH / "fixture"
RUNS = BENCH / "runs" / "forger"
MODEL = "qwen3.5:4b"
# パッケージ版(file://)からの fetch は Origin: null を送り Ollama の CORS で
# 403 になる + CSP(connect-src http://localhost:*)が 127.0.0.1 を許可しない。
# そのため localhost バインドの Origin 除去 + ACAO 付与プロキシを挟む
OLLAMA_URL = "http://localhost:11435"
OLLAMA_REAL = "127.0.0.1:11434"
TIMEOUT_SEC = 900
POLL_SEC = 2


class _CorsProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self._cors()
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def _forward(self) -> None:
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        conn = http.client.HTTPConnection(OLLAMA_REAL, timeout=600)
        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in ("origin", "host", "content-length",
                                        "connection", "accept-encoding")}
        conn.request(self.command, self.path, body=body, headers=headers)
        res = conn.getresponse()
        self.send_response(res.status)
        for k, v in res.getheaders():
            if k.lower() not in ("transfer-encoding", "content-length",
                                 "connection"):
                self.send_header(k, v)
        self._cors()
        if res.length is not None:
            self.send_header("Content-Length", str(res.length))
        else:
            self.close_connection = True  # HTTP/1.0: EOF で終端を通知
        self.end_headers()
        while True:
            chunk = res.read(8192)
            if not chunk:
                break
            self.wfile.write(chunk)
            self.wfile.flush()
        conn.close()

    do_GET = _forward
    do_POST = _forward
    do_DELETE = _forward

    def log_message(self, *args) -> None:
        pass


def start_cors_proxy() -> ThreadingHTTPServer:
    srv = ThreadingHTTPServer(("127.0.0.1", 11435), _CorsProxyHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def find_prompt(task: str) -> Path:
    matches = sorted((BENCH / "tasks").glob(f"{task}-*/prompt.txt"))
    if not matches:
        sys.exit(f"prompt not found: tasks/{task}-*/prompt.txt")
    return matches[0]


def prep_workdir(task: str, run_no: int) -> Path:
    run_dir = RUNS / task / f"run{run_no}"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(FIXTURE, run_dir, ignore=shutil.ignore_patterns("__pycache__"))
    return run_dir


def run_task(task: str, run_no: int = 1) -> dict:
    prompt = find_prompt(task).read_text(encoding="utf-8").strip()
    run_dir = prep_workdir(task, run_no)
    log_lines: list[str] = []

    def log(msg: str) -> None:
        line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        log_lines.append(line)

    result = {"task": task, "interventions": 0, "timed_out": False}
    port = 9222
    proxy = start_cors_proxy()

    with sync_playwright() as p:
        # playwright-python は _electron 未公開のため CDP 経由で接続
        env = os.environ.copy()
        env.pop("ELECTRON_RUN_AS_NODE", None)  # Devin 側 Electron からの継承を除去
        proc = subprocess.Popen(
            [str(TEASPOON_EXE), f"--remote-debugging-port={port}", str(run_dir)],
            env=env,
        )
        browser = None
        for _ in range(60):
            try:
                browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}")
                break
            except Exception:
                time.sleep(1)
        if browser is None:
            proc.kill()
            raise RuntimeError("CDP connect failed")
        page = None
        for _ in range(60):
            for ctx in browser.contexts:
                for pg in ctx.pages:
                    if not pg.url.startswith(("devtools://", "chrome-", "about:")):
                        page = pg
                        break
                if page:
                    break
            if page:
                break
            time.sleep(1)
        if page is None:
            proc.kill()
            raise RuntimeError("app page not found")
        page.set_default_timeout(15_000)
        log("app launched")

        # Ollama プロバイダを localStorage に事前設定して reload
        page.evaluate(
            """([model, url]) => {
                localStorage.setItem('llm_provider', 'ollama')
                localStorage.setItem('ollama_base_url', url)
                localStorage.setItem('ollama_model', model)
                // 同一projectPathの過去会話（前回失敗run等）を除去
                localStorage.removeItem('chat_conversations')
            }""",
            [MODEL, OLLAMA_URL],
        )
        # Electron の reload は renderer detach で ERR_ABORTED を投げることがある
        try:
            page.reload(wait_until="domcontentloaded")
        except Exception:
            pass
        page.wait_for_selector(".chat-input textarea", state="visible")
        # textarea は isLoading || !isConfigured で disabled → 有効化まで待機
        page.wait_for_selector(".chat-input textarea:not([disabled])", state="visible")
        log("configured: ollama " + MODEL)

        page.fill(".chat-input textarea", prompt)
        t0 = time.time()
        page.click(".send-button")
        log("prompt sent")

        idle_polls = 0
        while True:
            elapsed = time.time() - t0
            if elapsed > TIMEOUT_SEC:
                result["timed_out"] = True
                log(f"TIMEOUT after {TIMEOUT_SEC}s")
                break
            try:
                approve = page.query_selector(
                    ".file-edit-approval .approve-button"
                )
                if approve and approve.is_visible():
                    approve.click()
                    result["interventions"] += 1
                    log(f"approved edit/command batch (#{result['interventions']})")
                    continue
            except Exception:
                pass

            busy = page.query_selector(".cancel-button")
            textarea_disabled = page.get_attribute(".chat-input textarea", "disabled")
            if busy is None and textarea_disabled is None:
                idle_polls += 1
                if idle_polls >= 3:
                    log("idle -> done")
                    break
            else:
                idle_polls = 0
            time.sleep(POLL_SEC)

        result["duration_sec"] = int(time.time() - t0)
        log(f"finished in {result['duration_sec']}s, interventions={result['interventions']}")

        # 証跡: チャット内容のダンプ + スクリーンショット
        try:
            texts = page.eval_on_selector_all(
                ".chat-message .message-text", "els => els.map(e => e.innerText)"
            )
            log_lines.append("\n=== chat messages ===")
            log_lines.extend(texts)
        except Exception as e:
            log(f"chat dump failed: {e}")
        page.screenshot(path=str(run_dir / "screenshot.png"), full_page=True)
        proc.terminate()
        proxy.shutdown()

    (run_dir / "agent.log").write_text("\n".join(log_lines), encoding="utf-8")
    return result


def main() -> None:
    tasks = sys.argv[1:] or sys.exit("usage: python tools/run_teaspoon.py T1 [T2 ...]")
    for t in tasks:
        run_task(t)


if __name__ == "__main__":
    main()
