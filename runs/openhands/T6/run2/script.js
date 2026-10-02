document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const scoreDisplay = document.getElementById('score');
    const timerDisplay = document.getElementById('timer');
    const startButton = document.getElementById('start-button');
    const gameOverModal = document.getElementById('game-over-modal');
    const finalScoreDisplay = document.getElementById('final-score');
    const restartButton = document.getElementById('restart-button');

    let score = 0;
    let timeLeft = 30;
    let gameTimer = null;
    let moleTimer = null;
    let isPlaying = false;
    let lastCell = null;

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

        // Remove up class from all cells
        cells.forEach(cell => cell.classList.remove('up'));

        const targetCell = randomCell(cells);
        targetCell.classList.add('up');

        // Random duration for mole to stay up (between 600ms and 1000ms)
        const stayTime = Math.random() * 400 + 600;

        moleTimer = setTimeout(() => {
            if (isPlaying) {
                targetCell.classList.remove('up');
                showMole();
            }
        }, stayTime);
    }

    function startGame() {
        // Reset state
        score = 0;
        timeLeft = 30;
        scoreDisplay.textContent = score;
        timerDisplay.textContent = timeLeft;
        startButton.disabled = true;
        gameOverModal.classList.add('hidden');
        isPlaying = true;

        cells.forEach(cell => cell.classList.remove('up'));

        // Start mole spawning
        showMole();

        // Start countdown timer
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
        startButton.disabled = false;

        // Show game over modal with final score
        finalScoreDisplay.textContent = score;
        gameOverModal.classList.remove('hidden');
    }

    // Mole click event
    cells.forEach(cell => {
        const mole = cell.querySelector('.mole');
        mole.addEventListener('click', (e) => {
            if (!isPlaying) return;
            if (cell.classList.contains('up')) {
                score++;
                scoreDisplay.textContent = score;
                cell.classList.remove('up'); // hit and hide immediately
            }
        });
    });

    startButton.addEventListener('click', startGame);
    restartButton.addEventListener('click', startGame);
});
