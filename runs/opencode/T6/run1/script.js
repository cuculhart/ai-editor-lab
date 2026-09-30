const cells = document.querySelectorAll('.cell');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const startButton = document.getElementById('start-button');
const modal = document.getElementById('game-over-modal');
const finalScoreDisplay = document.getElementById('final-score');
const restartButton = document.getElementById('restart-button');

let score = 0;
let timeLeft = 30;
let gameTimer = null;
let moleTimer = null;
let isPlaying = false;
let lastCell = null;

function randomTime(min, max) {
    return Math.round(Math.random() * (max - min) + min);
}

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
    const time = randomTime(600, 1200);
    const cell = randomCell(cells);
    
    cell.classList.add('up');

    setTimeout(() => {
        cell.classList.remove('up');
        if (isPlaying) {
            moleTimer = setTimeout(showMole, randomTime(200, 600));
        }
    }, time);
}

function startGame() {
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    startButton.disabled = true;
    modal.classList.add('hidden');
    isPlaying = true;

    showMole();

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
    clearTimeout(moleTimer);
    
    cells.forEach(cell => cell.classList.remove('up'));

    finalScoreDisplay.textContent = score;
    modal.classList.remove('hidden');
    startButton.disabled = false;
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
restartButton.addEventListener('click', () => {
    modal.classList.add('hidden');
    startGame();
});
