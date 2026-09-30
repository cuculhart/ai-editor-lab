const cells = document.querySelectorAll('.cell');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const startButton = document.getElementById('start-button');

let score = 0;
let timeLeft = 30;
let gameInterval = null;
let moleTimer = null;
let isPlaying = false;
let lastCell = null;

// ランダムなマスを選ぶ（直前と同じマスは選ばない）
function randomCell(cells) {
    const index = Math.floor(Math.random() * cells.length);
    const cell = cells[index];
    if (cell === lastCell) {
        return randomCell(cells);
    }
    lastCell = cell;
    return cell;
}

// モグラをランダムに出現させる
function showMole() {
    if (!isPlaying) return;

    // すべてのマスからモグラを隠す
    cells.forEach(cell => cell.classList.remove('up'));

    // ランダムなマスにモグラを出す
    const targetCell = randomCell(cells);
    targetCell.classList.add('up');

    // モグラが出ている時間をランダムに設定 (600ms〜1200ms)
    const randomTime = Math.random() * 600 + 600;
    
    moleTimer = setTimeout(() => {
        targetCell.classList.remove('up');
        if (isPlaying) {
            // 次のモグラが出るまでの間隔 (200ms〜600ms)
            const nextTime = Math.random() * 400 + 200;
            setTimeout(showMole, nextTime);
        }
    }, randomTime);
}

// ゲーム開始
function startGame() {
    // 初期化
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    startButton.disabled = true;
    isPlaying = true;
    lastCell = null;

    // モグラ出現開始
    showMole();

    // タイマー開始 (1秒ごと)
    gameInterval = setInterval(() => {
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
    clearInterval(gameInterval);
    clearTimeout(moleTimer);

    // すべてのモグラを隠す
    cells.forEach(cell => cell.classList.remove('up'));

    // スタートボタンを再度有効化
    startButton.disabled = false;

    // 最終得点を表示
    alert(`タイムアップ！ 終了です。\nあなたの最終得点は ${score} 点です！`);
}

// マス（モグラ）をクリックしたときの処理
cells.forEach(cell => {
    cell.addEventListener('click', () => {
        if (!isPlaying) return;

        // モグラが出ている状態のマスをクリックした場合のみ得点加算
        if (cell.classList.contains('up')) {
            score++;
            scoreDisplay.textContent = score;
            cell.classList.remove('up'); // 叩いたらすぐに隠す
        }
    });
});

// スタートボタンのイベントリスナー
startButton.addEventListener('click', startGame);
