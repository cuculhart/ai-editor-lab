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
let moleTimeout = null;
let isPlaying = false;
let lastCell = null;

function startGame() {
    // リセット
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    gameOverModal.classList.add('hidden');
    startButton.disabled = true;
    isPlaying = true;

    // タイマー開始
    gameInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);

    // モグラ出現ループ開始
    showMoleRandomly();
}

function showMoleRandomly() {
    if (!isPlaying) return;

    // ランダムなセルを選択（前回と同じセルは避ける）
    let randomIndex;
    do {
        randomIndex = Math.floor(Math.random() * cells.length);
    } while (cells[randomIndex] === lastCell && cells.length > 1);

    const cell = cells[randomIndex];
    lastCell = cell;

    // モグラを出す
    cell.classList.add('up');

    // モグラが出ている時間（ランダム: 600ms 〜 1200ms）
    const stayDuration = Math.random() * 600 + 600;

    moleTimeout = setTimeout(() => {
        cell.classList.remove('up');
        
        // 次のモグラが出るまでのインターバル（ランダム: 200ms 〜 500ms）
        if (isPlaying) {
            const nextInterval = Math.random() * 300 + 200;
            setTimeout(showMoleRandomly, nextInterval);
        }
    }, stayDuration);
}

// モグラをクリックしたときの処理
cells.forEach(cell => {
    const mole = cell.querySelector('.mole');
    
    // タップやクリックの両方に対応
    const hitHandler = (e) => {
        e.preventDefault();
        if (!isPlaying) return;
        
        // モグラが出ていて、まだ叩かれていない（クラスupがついている）場合
        if (cell.classList.contains('up')) {
            score++;
            scoreDisplay.textContent = score;
            cell.classList.remove('up'); // すぐに隠す
        }
    };

    cell.addEventListener('mousedown', hitHandler);
    cell.addEventListener('touchstart', hitHandler);
});

function endGame() {
    isPlaying = false;
    clearInterval(gameInterval);
    clearTimeout(moleTimeout);

    // 全てのモグラを隠す
    cells.forEach(cell => cell.classList.remove('up'));

    // モーダルに最終得点を表示
    finalScoreDisplay.textContent = score;
    gameOverModal.classList.remove('hidden');
    startButton.disabled = false;
}

startButton.addEventListener('click', startGame);
restartButton.addEventListener('click', startGame);
