const cells = document.querySelectorAll('.cell');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const startButton = document.getElementById('start-button');
const gameOverModal = document.getElementById('game-over-modal');
const finalScoreDisplay = document.getElementById('final-score');
const restartButton = document.getElementById('restart-button');

let score = 0;
let timeLeft = 30;
let gameInterval = null;
let timerInterval = null;
let lastCell = null;
let isPlaying = false;

// ランダムにセルを選ぶ（前回と同じセルを避ける）
function randomCell(cells) {
    const index = Math.floor(Math.random() * cells.length);
    const cell = cells[index];
    if (cell === lastCell) {
        return randomCell(cells);
    }
    lastCell = cell;
    return cell;
}

// モグラを登場させる
function showMole() {
    if (!isPlaying) return;

    // すべてのセルからモグラクラスを削除
    cells.forEach(cell => cell.classList.remove('up'));

    // ランダムに選んだセルにモグラを表示
    const targetCell = randomCell(cells);
    targetCell.classList.add('up');

    // 表示時間をランダムに設定（例: 600ms〜1200msの間）
    const time = Math.random() * 600 + 600;
    
    gameInterval = setTimeout(() => {
        if (isPlaying) {
            showMole();
        }
    }, time);
}

// ゲーム開始
function startGame() {
    // 状態の初期化
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    isPlaying = true;
    startButton.disabled = true;
    gameOverModal.classList.add('hidden');

    // モグラ出現ループ開始
    showMole();

    // タイマー開始
    timerInterval = setInterval(() => {
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
    clearTimeout(gameInterval);
    clearInterval(timerInterval);

    // モグラをすべて隠す
    cells.forEach(cell => cell.classList.remove('up'));

    // スタートボタンを有効化
    startButton.disabled = false;

    // 最終得点を表示してモーダルを開く
    finalScoreDisplay.textContent = score;
    gameOverModal.classList.remove('hidden');
}

// モグラをクリックしたときの処理
cells.forEach(cell => {
    const mole = cell.querySelector('.mole');
    
    // セルまたはモグラをクリックしたときに得点を加算
    cell.addEventListener('click', () => {
        if (!isPlaying) return;
        // モグラが表示されている（.upクラスがついている）場合のみ得点加算
        if (cell.classList.contains('up')) {
            score++;
            scoreDisplay.textContent = score;
            // 叩かれたらすぐに隠す（連続クリック防止・スピード感のため）
            cell.classList.remove('up');
        }
    });
});

// イベントリスナーの登録
startButton.addEventListener('click', startGame);
restartButton.addEventListener('click', startGame);
