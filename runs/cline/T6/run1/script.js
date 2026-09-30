document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const startButton = document.getElementById('start-button');
    const timerDisplay = document.getElementById('timer');
    const scoreDisplay = document.getElementById('score');
    const gameOverMessage = document.getElementById('game-over-message');
    const finalScoreDisplay = document.getElementById('final-score');

    let score = 0;
    let timeLeft = 30;
    let gameTimer = null;
    let moleTimer = null;
    let isPlaying = false;
    let lastCell = null;

    // ランダムにセルを選ぶ（前回と同じセルを連続で選ばないようにする）
    function randomCell(cells) {
        const index = Math.floor(Math.random() * cells.length);
        const cell = cells[index];
        if (cell === lastCell) {
            return randomCell(cells);
        }
        lastCell = cell;
        return cell;
    }

    // ランダムな時間（ミリ秒）を返す
    function randomTime(min, max) {
        return Math.round(Math.random() * (max - min) + min);
    }

    // モグラをひょっこり出す
    function showMole() {
        if (!isPlaying) return;

        const time = randomTime(600, 1000); // モグラが出ている時間
        const cell = randomCell(cells);

        cell.classList.add('up');

        setTimeout(() => {
            cell.classList.remove('up');
            if (isPlaying) {
                // 次のモグラが出るまでの間隔
                const nextTime = randomTime(400, 800);
                moleTimer = setTimeout(showMole, nextTime);
            }
        }, time);
    }

    // ゲームスタート
    function startGame() {
        // 状態のリセット
        score = 0;
        timeLeft = 30;
        scoreDisplay.textContent = score;
        timerDisplay.textContent = timeLeft;
        gameOverMessage.classList.add('hidden');
        startButton.disabled = true;
        isPlaying = true;

        cells.forEach(cell => cell.classList.remove('up'));

        // モグラ出現開始
        showMole();

        // タイマー開始（1秒ごと）
        gameTimer = setInterval(() => {
            timeLeft--;
            timerDisplay.textContent = timeLeft;

            if (timeLeft <= 0) {
                endGame();
            }
        }, 1000);
    }

    // ゲーム終了
    function endGame() {
        isPlaying = false;
        clearInterval(gameTimer);
        clearTimeout(moleTimer);

        // 全てのモグラを隠す
        cells.forEach(cell => cell.classList.remove('up'));

        // 最終得点表示
        finalScoreDisplay.textContent = score;
        gameOverMessage.classList.remove('hidden');

        // スタートボタンを再度有効化
        startButton.disabled = false;
        startButton.textContent = 'もう一度プレイ';
    }

    // モグラをクリックしたときの処理
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            if (!isPlaying) return;
            // モグラが出ているセルをクリックしたか判定
            if (cell.classList.contains('up')) {
                score++;
                scoreDisplay.textContent = score;
                // 連続クリックを防ぐため、一度叩いたらすぐに隠す
                cell.classList.remove('up');
            }
        });
    });

    // スタートボタンのイベントリスナー
    startButton.addEventListener('click', startGame);
});
