const cells = document.querySelectorAll('.cell');
const startButton = document.getElementById('start-button');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const messageDisplay = document.getElementById('message');

let score = 0;
let timeLeft = 30;
let gameInterval = null;
let timerInterval = null;
let lastCell = null;

function getRandomCell() {
    const index = Math.floor(Math.random() * cells.length);
    const cell = cells[index];
    if (cell === lastCell) {
        return getRandomCell();
    }
    lastCell = cell;
    return cell;
}

function showMole() {
    const cell = getRandomCell();
    const mole = document.createElement('div');
    mole.classList.add('mole');
    cell.appendChild(mole);

    // モグラがせり上がる演出
    setTimeout(() => {
        mole.classList.add('up');
    }, 20);

    const hideTimeout = setTimeout(() => {
        mole.classList.remove('up');
        setTimeout(() => {
            if (mole.parentElement) {
                mole.remove();
            }
        }, 150);
    }, 850);

    mole.addEventListener('click', () => {
        if (!mole.classList.contains('up')) return;
        score++;
        scoreDisplay.textContent = score;
        clearTimeout(hideTimeout);
        mole.classList.remove('up');
        setTimeout(() => {
            if (mole.parentElement) {
                mole.remove();
            }
        }, 150);
    }, { once: true });
}

function startGame() {
    // リセット
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    messageDisplay.textContent = '';
    startButton.disabled = true;

    // 既存のモグラをクリア
    cells.forEach(cell => {
        cell.innerHTML = '';
    });

    // モグラ出現ループ (約1秒ごと)
    gameInterval = setInterval(() => {
        showMole();
    }, 900);

    // タイマーカウントダウン
    timerInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function endGame() {
    clearInterval(gameInterval);
    clearInterval(timerInterval);

    // 全てのモグラを隠す
    const moles = document.querySelectorAll('.mole');
    moles.forEach(mole => {
        mole.classList.remove('up');
    });

    startButton.disabled = false;
    messageDisplay.textContent = `ゲーム終了！ 最終得点: ${score}点`;
}

startButton.addEventListener('click', startGame);
