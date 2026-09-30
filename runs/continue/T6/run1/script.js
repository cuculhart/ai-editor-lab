document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const startButton = document.getElementById('start-button');
    const scoreDisplay = document.getElementById('score');
    const timerDisplay = document.getElementById('timer');
    const gameOverModal = document.getElementById('game-over-modal');
    const finalScoreDisplay = document.getElementById('final-score');
    const restartButton = document.getElementById('restart-button');

    let score = 0;
    let timeLeft = 30;
    let isPlaying = false;
    let timerInterval = null;
    let moleTimeout = null;
    let currentCell = null;

    // ゲーム開始
    function startGame() {
        // 初期化
        score = 0;
        timeLeft = 30;
        scoreDisplay.textContent = score;
        timerDisplay.textContent = timeLeft;
        isPlaying = true;
        
        startButton.disabled = true;
        gameOverModal.classList.add('hidden');

        // タイマー開始
        timerInterval = setInterval(() => {
            timeLeft--;
            timerDisplay.textContent = timeLeft;

            if (timeLeft <= 0) {
                endGame();
            }
        }, 1000);

        // モグラ出現ループ開始
        showRandomMole();
    }

    // ランダムにモグラを表示
    function showRandomMole() {
        if (!isPlaying) return;

        // 前のモグラを隠す
        if (currentCell) {
            currentCell.classList.remove('show');
            currentCell = null;
        }

        // ランダムにセルを選択 (前回と同じセルを避けるかランダム)
        const randomIndex = Math.floor(Math.random() * cells.length);
        const cell = cells[randomIndex];

        cell.classList.add('show');
        currentCell = cell;

        // モグラが出ている時間をランダムに設定 (0.6秒〜1.2秒)
        const stayTime = Math.random() * 600 + 600;

        moleTimeout = setTimeout(() => {
            if (isPlaying) {
                showRandomMole();
            }
        }, stayTime);
    }

    // モグラをクリックした時の処理
    cells.forEach(cell => {
        const mole = cell.querySelector('.mole');

        mole.addEventListener('click', (e) => {
            e.stopPropagation(); // セル自体のイベント伝播を防ぐ
            if (!isPlaying) return;

            // 表示中かつまだ叩かれていないモグラ判定（クラス名showが付いているとき）
            if (cell.classList.contains('show')) {
                score++;
                scoreDisplay.textContent = score;

                // 叩かれたらすぐに隠す
                cell.classList.remove('show');
                if (cell === currentCell) {
                    currentCell = null;
                }

                // タイマーをクリアして次のモグラを即座に出現させる
                clearTimeout(moleTimeout);
                showRandomMole();
            }
        });
    });

    // ゲーム終了
    function endGame() {
        isPlaying = false;
        clearInterval(timerInterval);
        clearTimeout(moleTimeout);

        // すべてのモグラを隠す
        cells.forEach(cell => {
            cell.classList.remove('show');
        });
        currentCell = null;

        // 最終スコアを表示してモーダルを開く
        finalScoreDisplay.textContent = score;
        gameOverModal.classList.remove('hidden');
        startButton.disabled = false;
    }

    // イベントリスナー
    startButton.addEventListener('click', startGame);
    restartButton.addEventListener('click', startGame);
});
