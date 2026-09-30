const cells = document.querySelectorAll('.cell');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const startButton = document.getElementById('start-button');
const modal = document.getElementById('game-over-modal');
const finalScoreDisplay = document.getElementById('final-score');
const restartButton = document.getElementById('restart-button');

let score = 0;
let timeLeft = 30;
let gameInterval = null;
let moleTimer = null;
let isPlaying = false;
let lastCell = null;

function startGame() {
    // Reset state
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    modal.classList.add('hidden');
    startButton.disabled = true;
    startButton.style.opacity = '0.6';
    isPlaying = true;

    // Clear any existing active moles
    cells.forEach(cell => cell.classList.remove('show'));

    // Start timer countdown
    gameInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);

    // Start popping up moles
    popupMole();
}

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

function popupMole() {
    if (!isPlaying) return;

    const time = randomTime(600, 1200); // How long mole stays up
    const cell = randomCell(cells);

    cell.classList.add('show');

    moleTimer = setTimeout(() => {
        cell.classList.remove('show');
        if (isPlaying) {
            popupMole();
        }
    }, time);
}

function hitMole(e) {
    if (!isPlaying) return;
    const cell = e.currentTarget;
    if (cell.classList.contains('show')) {
        score++;
        scoreDisplay.textContent = score;
        cell.classList.remove('show');
        
        // Visual feedback on hit
        const mole = cell.querySelector('.mole');
        mole.style.backgroundColor = '#ff6b6b';
        setTimeout(() => {
            mole.style.backgroundColor = '#a0522d';
        }, 150);
    }
}

function endGame() {
    isPlaying = false;
    clearInterval(gameInterval);
    clearTimeout(moleTimer);

    cells.forEach(cell => cell.classList.remove('show'));

    finalScoreDisplay.textContent = score;
    modal.classList.remove('hidden');

    startButton.disabled = false;
    startButton.style.opacity = '1';
}

// Event Listeners
cells.forEach(cell => {
    cell.addEventListener('click', hitMole);
});

startButton.addEventListener('click', startGame);
restartButton.addEventListener('click', startGame);
