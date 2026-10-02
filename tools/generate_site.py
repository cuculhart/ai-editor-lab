"""bench/site/ に静的サイトを生成する。
data/editors.json + results/*.json + reviews/*.json を読み、
未計測値 "?" はそのまま表示する。

usage: python tools/generate_site.py
"""
import html
import json
import shutil
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
SITE = BENCH / "site"

MARKS = {"○": "mark-yes", "◯": "mark-yes", "△": "mark-mid", "×": "mark-no"}

MATRIX_LABELS = {
    "form": "形態",
    "os_windows": "Windows",
    "os_mac": "macOS",
    "os_linux": "Linux",
    "byok": "BYOK",
    "custom_endpoint": "カスタムエンドポイント",
    "local_llm": "ローカルLLM",
    "proxy_key_hiding": "プロキシでキー隠蔽",
    "token_saving": "トークン節約",
    "telemetry": "テレメトリー",
    "auto_approve": "自動実行",
    "parallel": "マルチターミナル/並走",
    "checkpoint": "やりなおし",
    "mcp": "MCP 対応",
    "cost_display": "コスト表示",
    "account_required": "アカウント登録",
    "target_audience": "ターゲット層",
}

SCORE_LABELS = {
    "audience": "ターゲット層の明確さ",
    "ui": "画面の見やすさ",
    "learning": "学習コスト",
    "steering": "エージェントの操縦性",
    "stuck_free": "詰まりにくさ",
    "error_handling": "エラー時の挙動",
    "speed_feel": "体感速度",
    "overall": "総合評価",
}

INSTALL_LABELS = {
    "time_min": "所要時間（分）",
    "steps": "手順数",
    "deps": "依存要件",
    "hw_spec": "必要スペック",
    "difficulty": "難易度",
    "notes": "導入メモ",
}

REVIEWER_ORDER = ["ChatGPT", "Gemini", "Claude", "Devin (SWE-2)"]

INDEX_MATRIX_KEYS = [
    "os_windows", "byok", "local_llm", "telemetry",
    "auto_approve", "parallel", "checkpoint",
]


def esc(v) -> str:
    return html.escape(str(v))


def val(v) -> str:
    if v == "?" or v is None:
        return '<span class="unknown">?</span>'
    if v in MARKS:
        return f'<span class="mark {MARKS[v]}">{esc(v)}</span>'
    if v is True:
        return '<span class="mark mark-yes">○</span>'
    if v is False:
        return '<span class="mark mark-no">×</span>'
    return esc(v)


def symbol_only(v) -> str:
    """一覧表では記号のみ表示。補足コメントは title ツールチップに残す。"""
    if v is None or v == "?":
        return val(v)
    s = str(v)
    if s[0] in MARKS or s[0] == "◎":
        mark = s[0]
        cls = MARKS.get(mark, "mark-yes")
        return f'<span class="mark {cls}" title="{esc(s)}">{esc(mark)}</span>'
    return val(v)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def page(title: str, body: str, base: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} — AIエディターラボ</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="container d-flex justify-content-between align-items-center">
    <a class="site-logo" href="{base}index.html">🧪 AIエディターラボ</a>
    <nav class="site-nav">
      <a href="{base}index.html">トップ</a>
      <a href="{base}method.html">測定方法</a>
      <a href="{base}article-harness.html">記事</a>
      <a href="{base}about.html">運営者について</a>
    </nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="container">
    <p>「?」は計測・調査中の値です。測定方法・生データはすべて公開しています。</p>
    <p>&copy; 2026 AIエディターラボ（運営: cuculhart管理者）</p>
  </div>
</footer>
</body>
</html>
"""


def _measured(run):
    # success=="?" は未計測のプレースホルダ。サイトには出さない（データには残す）
    return run.get("success") != "?"


def ranking_table(editors, results_map, category, cat_label, base=""):
    members = [
        e for e in editors
        if any(r["category"] == category and _measured(r)
               for r in results_map.get(e["id"], {}).get("runs", []))
    ]
    if not members:
        return f"<p class='text-muted'>{esc(cat_label)}に該当するツールはまだありません。</p>"
    rows = []
    for e in members:
        runs = [r for r in results_map[e["id"]]["runs"]
                if r["category"] == category and _measured(r)]
        # Score only the latest 2 runs per task: improvement lands quickly
        # (2 consecutive passes -> 100%) while a single lucky pass stays 50%.
        # Older runs remain visible in each editor's detail table.
        by_task: dict[str, list] = {}
        for r in runs:
            by_task.setdefault(r["task"], []).append(r)
        ok_n = total = 0
        for trs in by_task.values():
            trs.sort(key=lambda r: (str(r.get("date", "")), r.get("run", 0)))
            recent = trs[-2:]
            ok_n += sum(1 for r in recent if r.get("success") is True or r.get("success") == "○")
            total += len(recent)
        rows.append((e, ok_n, total))
    rows.sort(key=lambda t: (t[1] / t[2], t[1]), reverse=True)
    body_rows = ""
    for e, ok_n, total in rows:
        pct = round(100 * ok_n / total)
        success = f"{ok_n} / {total} （{pct}%）"
        body_rows += (
            "<tr>"
            f"<td class='editor-name'><a href='{base}editors/{e['id']}.html'>{esc(e['name'])}</a>"
            f"<br><small class='text-muted'>{esc(e['form'])}</small></td>"
            f"<td>{success}</td>"
            "</tr>"
        )
    return (
        "<div class='table-responsive'><table class='table table-pop mb-0'>"
        "<thead><tr><th>ツール</th><th>成功数/試行数（成功率・各タスク直近2回まで集計）</th></tr></thead>"
        f"<tbody>{body_rows}</tbody></table></div>"
    )


def matrix_table(editors, reviews_map, base=""):
    head = "".join(f"<th>{esc(MATRIX_LABELS[k])}</th>" for k in INDEX_MATRIX_KEYS)
    rows = []
    for e in editors:
        m = reviews_map.get(e["id"], {}).get("matrix", {})
        cells = "".join(f"<td class='text-center'>{symbol_only(m.get(k, '?'))}</td>" for k in INDEX_MATRIX_KEYS)
        rows.append(
            f"<tr><td class='editor-name'><a href='{base}editors/{e['id']}.html'>{esc(e['name'])}</a></td>{cells}</tr>"
        )
    return (
        "<div class='table-responsive'><table class='table table-pop mb-0'>"
        f"<thead><tr><th>ツール</th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
    )


def review_score_table(editors, reviews_map, base=""):
    rows = []
    for e in editors:
        revs = reviews_map.get(e["id"], {}).get("usability_reviews", [])
        overalls = {
            rv["reviewer"]: rv.get("scores", {}).get("overall")
            for rv in revs
        }
        nums = [s for s in overalls.values() if isinstance(s, (int, float))]
        avg = sum(nums) / len(nums) if nums else None
        rows.append((e, overalls, avg))
    rows.sort(key=lambda t: (t[2] is not None, t[2]), reverse=True)

    def cell(score):
        if isinstance(score, (int, float)):
            return f"{score:g}"
        return val("?")

    body_rows = "".join(
        "<tr>"
        f"<td class='editor-name'><a href='{base}editors/{e['id']}.html'>{esc(e['name'])}</a></td>"
        f"<td class='text-center'><strong>{f'{avg:.1f}' if avg is not None else '?'}</strong></td>"
        + "".join(
            f"<td class='text-center'>{cell(overalls.get(r))}</td>"
            for r in REVIEWER_ORDER
        )
        + "</tr>"
        for e, overalls, avg in rows
    )
    head = "".join(f"<th class='text-center'>{esc(r)}</th>" for r in REVIEWER_ORDER)
    return (
        "<div class='table-responsive'><table class='table table-pop mb-0'>"
        f"<thead><tr><th>製品名</th><th class='text-center'>平均スコア</th>{head}</tr></thead>"
        f"<tbody>{body_rows}</tbody></table></div>"
    )


def index_page(data, results_map, reviews_map):
    editors = data["editors"]
    cats = data["categories"]

    months = sorted({
        r["date"][:7]
        for res in results_map.values() for r in res.get("runs", [])
        if _measured(r) and isinstance(r.get("date"), str) and len(r["date"]) >= 7
    })
    if months:
        def ym(m):
            return f"{m[:4]}年{int(m[5:7])}月"
        period = ym(months[0]) if months[0] == months[-1] else f"{ym(months[0])}〜{ym(months[-1])}"
        measured_at = f"計測: {period}"
    else:
        measured_at = "計測: 準備中"

    cat_sections = ""
    for cat_id, cat_label in cats.items():
        model = data["models"].get(cat_id, "")
        cat_sections += f"""
  <section class="section">
    <div class="container">
      <h2>🏆 {esc(cat_label)} <small class="text-muted fs-6">{esc(model)}</small></h2>
      {ranking_table(editors, results_map, cat_id, cat_label)}
      <p class="small text-muted mt-2 mb-0">
        ※ 成功率は各タスクの<strong>直近2回の試行</strong>のみを集計（2連続合格で100%、1回だけの成功は50%）。古い試行は各ツールの詳細表に全履歴として残ります。
        また T3（リファクタリング）は受入テストを強化し、成果物がベースラインと同一の「no-op 合格」は不合格に訂正しています
        （詳細: <a href="method.html">測定方法</a>）。
      </p>
    </div>
  </section>"""
    cards = "".join(
        f"""<div class="col-md-4 mb-3"><a class="card-link" href="editors/{e['id']}.html">
        <div class="card-pop"><div class="editor-name">{esc(e['name'])}</div>
        <div class="text-muted small">{esc(e['form'])} / {esc(e['license'])}</div>
        <p class="mb-0 mt-2 small">{esc(e['notes'])}</p></div></a></div>"""
        for e in editors
    )
    body = f"""
  <section class="hero">
    <div class="container">
      <span class="hero-badge">BYOK・エージェント型のみ集めました</span>
      <h1>{esc(data['site']['name'])}</h1>
      <p class="lead">{esc(data['site']['tagline'])}</p>
      <p class="mb-0"><small class="text-muted">{measured_at} ｜ Windows 11 + Ryzen 5 4500U の一般的なPCで実測</small></p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="card-pop">
        <strong>このサイトの比較対象は「エージェント型」だけです。</strong>
        ファイルの読み書き・コマンド実行まで自律で回るツールのみを集めています。
        補完・チャット補助型（GitHub Copilot 等）や、月額サブスクの大手有料ツール
        （Claude Code / Devin / Cursor 等）は対象外です。
      </div>
    </div>
  </section>
{cat_sections}
  <section class="section">
    <div class="container">
      <h2>📋 機能マトリクス</h2>
      {matrix_table(editors, reviews_map)}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>⭐ 4者レビュー（初学者におすすめ度・0〜5）</h2>
      {review_score_table(editors, reviews_map)}
      <p class="small text-muted mt-2 mb-0">
        ※ ChatGPT / Gemini / Claude は本サイトの実測データ（結果・ログ）を読んで採点したレビューで、
        各AIが実際にツールを操作した評価ではありません。Devin (SWE-2) は本ベンチの計測実行者です。
      </p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>🧰 対象ツール一覧（{len(editors)} 本）</h2>
      <div class="row">{cards}</div>
    </div>
  </section>"""
    return page("トップ", body)


def editor_page(data, editor, results, reviews):
    base = "../"
    info_rows = "".join(
        f"<tr><th>{esc(k)}</th><td>{v}</td></tr>"
        for k, v in [
            ("形態", esc(editor["form"])), ("ライセンス", esc(editor["license"])),
            ("公式サイト", f"<a href='{esc(editor['url'])}'>{esc(editor['url'])}</a>" if editor["url"] != "?" else val("?")),
            ("リポジトリ", f"<a href='{esc(editor['repo'])}'>{esc(editor['repo'])}</a>" if editor["repo"] != "?" else val("?")),
            ("メモ", esc(editor["notes"])),
        ]
    )

    def split_mark(v):
        if v is None or v == "?":
            return val("?"), ""
        s = str(v)
        if s[0] in MARKS or s[0] == "◎":
            mark = s[0]
            cls = MARKS.get(mark, "mark-yes")
            desc = s[1:].lstrip(" 　")
            return f'<span class="mark {cls}">{esc(mark)}</span>', esc(desc)
        return "", esc(s)

    m = reviews.get("matrix", {})
    matrix_rows = "".join(
        "<tr><th>{}</th><td class='text-center'>{}</td><td>{}</td></tr>".format(
            esc(MATRIX_LABELS.get(k, k)), *split_mark(m.get(k, "?"))
        )
        for k in MATRIX_LABELS
    )

    inst = reviews.get("install", {})
    install_rows = "".join(
        f"<tr><th>{esc(INSTALL_LABELS.get(k, k))}</th><td>{val(inst.get(k, '?'))}</td></tr>"
        for k in INSTALL_LABELS
    )

    run_rows = ""
    sorted_runs = sorted(
        results.get("runs", []),
        key=lambda r: (0 if str(r.get("task", "")).startswith("T") else 1,
                       r.get("task", ""), r.get("category", ""),
                       str(r.get("date", "")), r.get("run", 0)),
    )
    for r in sorted_runs:
        if not _measured(r):
            continue
        cat_label = data["categories"].get(r["category"], r["category"])
        run_rows += (
            "<tr>"
            f"<td>{esc(r['task'])}</td><td>{esc(cat_label)}</td><td>{r['run']}</td>"
            f"<td>{val(r['success'])}</td><td>{val(r['duration_sec'])}</td>"
            f"<td>{val(r['cost_usd'])}</td><td>{val(r['interventions'])}</td>"
            f"<td>{val(r['date'])}</td>"
            "</tr>"
        )

    review_cards = ""
    sorted_reviews = sorted(
        reviews.get("usability_reviews", []),
        key=lambda rv: REVIEWER_ORDER.index(rv["reviewer"])
        if rv["reviewer"] in REVIEWER_ORDER else len(REVIEWER_ORDER),
    )
    for rv in sorted_reviews:
        score_cells = "".join(
            f"<tr><td>{esc(SCORE_LABELS.get(k, k))}</td><td class='score-num'>{val(rv['scores'].get(k, '?'))}</td></tr>"
            for k in SCORE_LABELS
        )
        review_cards += f"""
      <div class="col-md-6 mb-3"><div class="card-pop">
        <span class="reviewer-chip">{esc(rv['reviewer'])}</span>
        <table class="table table-sm mt-2 mb-2">{score_cells}</table>
        <p class="small mb-0">💬 {val(rv['comment'])}</p>
      </div></div>"""

    body = f"""
  <section class="section">
    <div class="container">
      <h2>{esc(editor['name'])}</h2>
      <div class="row">
        <div class="col-md-5 mb-3"><div class="card-pop"><h5>基本情報</h5>
          <table class="table table-sm">{info_rows}</table></div></div>
        <div class="col-md-7 mb-3"><div class="card-pop"><h5>導入の容易さ</h5>
          <table class="table table-sm">{install_rows}</table></div></div>
      </div>
      <div class="card-pop mb-3"><h5>機能マトリクス</h5>
        <div class="table-responsive"><table class="table table-sm">
        <thead><tr><th>項目</th><th class="text-center">評価</th><th>備考</th></tr></thead>
        <tbody>{matrix_rows}</tbody></table></div></div>
      <div class="card-pop mb-3"><h5>定量ベンチ結果</h5>
        <div class="table-responsive"><table class="table table-sm">
        <thead><tr><th>タスク</th><th>カテゴリ</th><th>回</th><th>成功</th><th>秒</th><th>USD</th><th>介入</th><th>日付</th></tr></thead>
        <tbody>{run_rows}</tbody></table></div></div>
      <h5 class="mt-4 mb-3">使用感レビュー（4者）</h5>
      <div class="row">{review_cards}</div>
    </div>
  </section>"""
    return page(editor["name"], body, base)


def method_page(data):
    task_rows = ""
    for task_dir in sorted((BENCH / "tasks").iterdir()):
        if not task_dir.is_dir() or not (task_dir / "prompt.txt").exists():
            continue
        prompt = (task_dir / "prompt.txt").read_text(encoding="utf-8").strip()
        task_rows += (
            f"<tr><td class='editor-name'>{esc(task_dir.name)}</td>"
            f"<td><pre class='mb-0 small' style='white-space:pre-wrap'>{esc(prompt)}</pre></td></tr>"
        )
    body = f"""
  <section class="section">
    <div class="container">
      <h2>📏 測定方法</h2>
      <div class="card-pop mb-3">
        <h5>公平性のルール</h5>
        <ul>
          <li>バックエンドモデルを統一: <strong>{esc(data['models']['byok-gemini'])}</strong>（ローカル系は <strong>{esc(data['models']['localllm'])}</strong>）</li>
          <li>プロンプトはタスクごとに文言固定・全文公開（下表）</li>
          <li>承認操作は「介入回数」として記録。自動承認可能なツールは自動承認ONで統一</li>
          <li>成功率は<strong>タスクごと直近2回の試行</strong>のみ集計。やり直しの古い失敗は分母に残さず、2連続合格すれば100%になる一方、1回だけの偶然的成功は50%止まりにします。古い試行は詳細表に全履歴として公開</li>
          <li>生データ（結果 JSON・diff・ログ）は公開リポジトリで全公開</li>
        </ul>
      </div>
      <div class="card-pop mb-3">
        <h5>測定指標</h5>
        <ul>
          <li>成功率（受入テスト通過）/ 所要時間 / トークン消費・コスト / 介入回数 / 成果物 diff</li>
          <li>使用感スコア（5段階）: ChatGPT・Gemini・Claude・Devin(SWE-2) の4者で評価。
            外部AIは同一の実測データを読んで採点する方式。Devin (SWE-2) は計測実行者</li>
        </ul>
      </div>
      <div class="card-pop mb-3">
        <h5>受入テスト（accept.py）と判定の訂正</h5>
        <ul>
          <li>各タスクの「成功」は同梱の accept.py が pass を返したことで判定。テスト不変・公開API互換・成果物の実在を検査します</li>
          <li><strong>T3 は 2026-10-02 に強化</strong>: 従来は「API互換 + TestCart 全パス」のみを見ていたため、ファイルを実質変更しない no-op でも合格し得る弱点がありました。現在は <code>real_refactor</code> 判定を追加し、(a) cart.py がベースラインとバイト同一、(b) 内部構造が「1個につき1要素」のリストのまま、のいずれかなら不合格とします</li>
          <li>強化後の再検証により、過去に成功と記録していた一部の実行が no-op と判明し訂正されました（Teaspoon run3、ZooCode T3）。訂正は各結果 JSON の notes にも記録しています</li>
        </ul>
      </div>
      <div class="card-pop mb-3">
        <h5>測定環境</h5>
        <ul>
          <li>Windows 11 Pro / <strong>Ryzen 5 4500U（APU・内蔵GPUのみ）</strong> / メモリ 32GB / GPUなし（ローカルLLMはCPU推論・常時100%）</li>
          <li>Ollama 0.21.0 / qwen3.5:4b（Q4_K_M, 6.8GB）</li>
          <li>ローカルLLM計測中のメモリ使用率は最大49%（約16GB）→ 24GB搭載機でも動作可能と見込まれる</li>
        </ul>
      </div>
      <div class="card-pop mb-3">
        <h5>観察: 成功率の差はモデルではなく「ハーネス」</h5>
        <p class="small">BYOK系は全ツール同一モデル（gemini-3.5-flash-lite）で計測しているため、ツール間の成功率差はモデル性能ではなく<strong>エージェントハーネス（ツール側の指示・フィードバック・完了判定の設計）</strong>の差を表します。T3（リファクタリング）の繰り返し計測で観察された失敗パターン:</p>
        <ul>
          <li><strong>no-op 完了報告</strong>: 編集に失敗した後、再試行せず読み取りやテスト実行だけを行い「リファクタリングを行いました」と報告（Teaspoon run3/5/9、ZooCode T3）。ファイルはベースラインとバイト同一でした</li>
          <li><strong>検証済みの事実と矛盾する実装</strong>: モデル自身が <code>hash(Product)</code> を実行してハッシュ不可（exit 1）を確認した直後に、<code>dict[Product, int]</code> を実装として書いたケース（Teaspoon run11）</li>
          <li><strong>結果と矛盾する完了報告</strong>: 直前のテスト実行が exit 1 なのに「全テストパスを確認しました」と報告</li>
        </ul>
        <p class="small">Cline 系（Cline・KiloCode・Roo Code）が同じモデルで安定する要因として、完了に専用ツール呼び出し（attempt_completion）を必須とする設計、編集後のファイル内容を毎回モデルへ返すフィードバック、詳細なシステムプロンプトなど「嘘の完了報告を構造的に通さない」仕組みが挙げられます。一方でこれらはトークン消費を増やす設計でもあります。Teaspoon IDE はこの観察をもとに、失敗した編集の未解決追跡・毎ステップの督促・虚偽報告時のユーザー警告を実装し改善を進めています。詳しい考察は<a href="article-harness.html">記事版</a>をご覧ください。</p>
      </div>
      <div class="card-pop">
        <h5>タスクと固定プロンプト</h5>
        <table class="table">{task_rows}</table>
      </div>
    </div>
  </section>"""
    return page("測定方法", body)


def article_page():
    # HTML version of site/plan/zenn-harness-article.txt (Zenn draft).
    # Update both when revising the article.
    body = """
  <section class="section">
    <div class="container" style="max-width: 820px">
      <h2>同じLLMを使っているのに成功率が全然違う — AIコーディングツールの差は「ハーネス」だった</h2>
      <p class="text-muted">公開実験ノート | 計測: 2026-10</p>

      <p>AIコーディングエージェントを同一タスク・同一モデルで実測比較する当サイトの計測で、<strong>同じLLMを使っているはずなのにツールによって成功率がまるで違う</strong>という現象が観察されました。繰り返し計測の末に分かったのは、差を生んでいたのはモデルではなく「<strong>ハーネス</strong>」（モデルを囲むツール側の仕組み）だったという話です。</p>

      <h4 class="mt-4">前提: 実験の条件</h4>
      <ul>
        <li><strong>モデルは全ツール共通</strong>: gemini-3.5-flash-lite（BYOK）</li>
        <li><strong>T3（リファクタリング）</strong>: Python のショッピングカートクラスを「1個ずつリストに追加」から「数量を管理する構造」へ書き換える。公開メソッド維持・テスト変更禁止・既存テスト全パスが条件</li>
      </ul>

      <h4 class="mt-4">観察された「嘘」3パターン</h4>
      <div class="card-pop mb-3">
        <h6>1. no-op 完了報告</h6>
        <p>差分編集（EDIT_FILE）が1回失敗したあと、再試行せず読み取りやテスト実行だけを行い、最後に「リファクタリングしました。主な変更内容: データ構造の刷新…」と報告。実際のファイルは<strong>ベースラインとバイト単位で同一</strong>。「API互換+テストパス」だけを見る受入テストではこれが合格してしまい、実際に過去の結果が訂正される事態になりました。</p>
      </div>
      <div class="card-pop mb-3">
        <h6>2. 検証済みの事実と矛盾する実装</h6>
        <p>モデル自身が <code>hash(Product)</code> を2回実行してハッシュ不可（exit 1）を確認した<strong>直後</strong>に、辞書のキーに使えない <code>dict[Product, int]</code> を実装として書いたケース。確認した事実と行動が完全に矛盾しています。</p>
      </div>
      <div class="card-pop mb-3">
        <h6>3. 結果と矛盾する完了報告</h6>
        <p>テスト実行が exit code 1 で終わった直後に「すべての既存テストがパスすることを確認しました」と報告。出力は目の前にあるのに、報告は正反対です。</p>
      </div>

      <h4 class="mt-4">なぜ Cline 系では起きにくいのか</h4>
      <p>同じモデルで Cline・KiloCode は安定して成功しました。違いはモデルではなくハーネスの設計です:</p>
      <table class="table">
        <thead><tr><th>仕組み</th><th>Cline 系</th><th>素朴な実装</th></tr></thead>
        <tbody>
          <tr><td>完了宣言</td><td><code>attempt_completion</code> ツール呼び出しが必須</td><td>コマンドを出さなければ完了扱い</td></tr>
          <tr><td>編集結果</td><td>編集後のファイル内容/diffを毎回モデルに返す</td><td>成否メッセージのみ</td></tr>
          <tr><td>環境情報</td><td>毎ターン environment_details を注入</td><td>なし</td></tr>
          <tr><td>プロンプト</td><td>数百行の詳細な振る舞い指示</td><td>短いプロトコル説明</td></tr>
        </tbody>
      </table>
      <p>「編集が失敗した」「ファイルが変わっていない」という事実が毎ターン突き合わせされる構造では、嘘の完了報告は通しにくくなります。一方、リッチなフィードバックはトークン消費を増やすトレードオフでもあります。</p>

      <h4 class="mt-4">対策: ハーネス側でできること</h4>
      <p>この観察をもとに Teaspoon IDE（当サイト運営者の自作 IDE）に実装した対策:</p>
      <ol>
        <li><strong>失敗した編集を「未解決」として追跡</strong> — 後続のテスト成功では解除しない</li>
        <li><strong>未解決の間は毎ステップ督促</strong> — 「対象ファイルはディスク上で未変更」と継続メッセージに注入</li>
        <li><strong>完了宣言時のnudge</strong> — 未解決のまま完了しようとしたら一度だけ突き返す</li>
        <li><strong>それでも嘘をついたらユーザーに警告</strong> — 「報告された変更はディスク上に存在しない可能性があります」と表示</li>
      </ol>
      <p>4番が重要です。<strong>モデルの正直性に頼るのではなく、事実をユーザーに見せる</strong>設計に倒しました — nudge を受けても虚偽報告を押し通すケースが実際にあったためです。</p>

      <h4 class="mt-4">教訓</h4>
      <ul>
        <li><strong>ツール比較はモデル比較ではない</strong>: 同一モデルで計測して初めて見えるのはハーネス性能</li>
        <li><strong>小さいモデルこそハーネスが効く</strong>: flash-lite 級ではフィードバック設計の差が成功率に直結する</li>
        <li><strong>受入テストは no-op を通し得る</strong>: 「テストがパスした」だけでは「仕事をした」ことにならない</li>
        <li><strong>リッチなハーネスにはコストがかかる</strong>: 軽量さと誠実さの両立が設計の腕の見せどころ</li>
      </ul>
      <p class="small text-muted mt-4">この記事の内容は <a href="method.html">測定方法</a> の観察カードの詳細版です。全試行の生データは各ツール詳細ページの履歴表をご覧ください。</p>
    </div>
  </section>"""
    return page("記事: ハーネス差", body)


def about_page(data):
    repo = data["site"].get("repo", "?")
    repo_html = (
        f"<a href='{esc(repo)}'>{esc(repo)}</a>" if repo != "?" else val("?")
    )
    body = f"""
  <section class="section">
    <div class="container">
      <h2>🙋 運営者について</h2>
      <div class="card-pop">
        <p>このサイトは <strong>cuculhart管理者</strong> が個人で運営する検証サイトです。</p>
        <ul>
          <li>測定に使ったプロンプト・タスク・受入テスト・結果の生データをすべて公開しています</li>
          <li>採点基準は各ページの「測定方法」に記載。誰でも同じ手順で追試できます</li>
          <li>比較対象に Teaspoon IDE（旧称 Forger、cuculhart の製品）を含みますが、他ツールと同一条件・同一基準で計測しています</li>
        </ul>
        <p class="mb-0 small text-muted">生データリポジトリ: {repo_html}</p>
      </div>
    </div>
  </section>"""
    return page("運営者について", body)


def main() -> None:
    data = load_json(BENCH / "data" / "editors.json")
    results_map = {}
    reviews_map = {}
    for p in (BENCH / "results").glob("*.json"):
        results_map[p.stem] = load_json(p)
    for p in (BENCH / "reviews").glob("*.json"):
        reviews_map[p.stem] = load_json(p)

    (SITE / "editors").mkdir(parents=True, exist_ok=True)
    (SITE / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(BENCH / "tools" / "assets" / "style.css", SITE / "assets" / "style.css")

    (SITE / "index.html").write_text(index_page(data, results_map, reviews_map), encoding="utf-8")
    (SITE / "method.html").write_text(method_page(data), encoding="utf-8")
    (SITE / "article-harness.html").write_text(article_page(), encoding="utf-8")
    (SITE / "about.html").write_text(about_page(data), encoding="utf-8")
    for e in data["editors"]:
        html_text = editor_page(
            data, e,
            results_map.get(e["id"], {"runs": []}),
            reviews_map.get(e["id"], {}),
        )
        (SITE / "editors" / f"{e['id']}.html").write_text(html_text, encoding="utf-8")
        print(f"generated: editors/{e['id']}.html")
    print("done ->", SITE)


if __name__ == "__main__":
    main()
