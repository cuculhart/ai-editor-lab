const cells = document.querySelectorAll('.cell');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const startButton = document.getElementById('start-button');
const gameOverPanel = document.getElementById('game-over');
const finalScoreDisplay = document.getElementById('final-score');

let score = 0;
let timeLeft = 30;
let gameInterval = null;
let moleTimeout = null;
let isPlaying = false;
let currentCell = null;

function startGame() {
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    gameOverPanel.classList.add('hidden');
    startButton.disabled = true;
    isPlaying = true;

    gameInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);

    showMole();
}

function randomCell(cells) {
    const index = Math.floor(Math.random() * cells.length);
    const cell = cells[index];
    if (cell === currentCell) {
        return randomCell(cells);
    }
    return cell;
}

function showMole() {
    if (!isPlaying) return;

    if (currentCell) {
        currentCell.classList.remove('show');
    }

    currentCell = randomCell(cells);
    currentCell.classList.add('show');

    const duration = Math.random() * 400 + 600;

    moleTimeout = setTimeout(() => {
        if (isPlaying) {
            showMole();
        }
    }, duration);
}

function whackMole(e) {
    if (!isPlaying) return;
    const cell = e.currentTarget;
    if (cell === currentCell && cell.classList.contains('show')) {
        score++;
        scoreDisplay.textContent = score;
        cell.classList.remove('show');
        clearTimeout(moleTimeout);
        showMole();
    }
}

function endGame() {
    isPlaying = false;
    clearInterval(gameInterval);
    clearTimeout(moleTimeout);

    if (currentCell) {
        currentCell.classList.remove('show');
    }

    finalScoreDisplay.textContent = score;
    gameOverPanel.classList.remove('hidden');
    startButton.disabled = false;
}

cells.forEach(cell => {
    cell.addEventListener('click', whackMole);
});

startButton.addEventListener('click', startGame);
