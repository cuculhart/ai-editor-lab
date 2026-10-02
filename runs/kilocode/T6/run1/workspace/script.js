const cells = document.querySelectorAll('.cell');
const startButton = document.getElementById('start-button');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const gameOverMessage = document.getElementById('game-over-message');

let score = 0;
let timeLeft = 30;
let gameTimer = null;
let moleTimer = null;
let lastCell = null;
let isPlaying = false;

function randomCell(cells) {
    const index = Math.floor(Math.random() * cells.length);
    const cell = cells[index];
    if (cell === lastCell) {
        return randomCell(cells);
    }
    lastCell = cell;
    return cell;
}

function showMole() {
    if (!isPlaying) return;
    
    const cell = randomCell(cells);
    cell.classList.add('up');

    const time = Math.random() * 600 + 400; // 400ms 〜 1000ms
    setTimeout(() => {
        cell.classList.remove('up');
    }, time);
}

function startGame() {
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    gameOverMessage.textContent = '';
    gameOverMessage.classList.add('hidden');
    startButton.disabled = true;
    isPlaying = true;

    moleTimer = setInterval(showMole, 600);

    gameTimer = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function endGame() {
    isPlaying = false;
    clearInterval(gameTimer);
    clearInterval(moleTimer);

    cells.forEach(cell => cell.classList.remove('up'));

    startButton.disabled = false;
    gameOverMessage.textContent = `ゲーム終了！ 最終得点: ${score}点`;
    gameOverMessage.classList.remove('hidden');
}

cells.forEach(cell => {
    cell.addEventListener('click', () => {
        if (!isPlaying) return;
        if (cell.classList.contains('up')) {
            score++;
            scoreDisplay.textContent = score;
            cell.classList.remove('up');
        }
    });
});

startButton.addEventListener('click', startGame);
