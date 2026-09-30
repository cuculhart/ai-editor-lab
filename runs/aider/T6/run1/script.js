const cells = document.querySelectorAll('.cell');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const startButton = document.getElementById('start-button');

let score = 0;
let timeLeft = 30;
let gameTimer = null;
let moleTimer = null;
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
    const time = Math.random() * 600 + 400; // 400ms 〜 1000ms の間表示
    const cell = randomCell(cells);
    cell.classList.add('up');

    setTimeout(() => {
        cell.classList.remove('up');
        if (timeLeft > 0) {
            moleTimer = setTimeout(showMole, Math.random() * 400 + 200);
        }
    }, time);
}

function startGame() {
    // 初期化
    score = 0;
    timeLeft = 30;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    startButton.disabled = true;
    
    cells.forEach(cell => cell.classList.remove('up'));

    // モグラ出現ループ開始
    showMole();

    // タイマー開始
    gameTimer = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(gameTimer);
            clearTimeout(moleTimer);
            cells.forEach(cell => cell.classList.remove('up'));
            alert(`ゲーム終了！あなたの得点は ${score} 点です。`);
            startButton.disabled = false;
        }
    }, 1000);
}

cells.forEach(cell => {
    cell.addEventListener('click', () => {
        if (!cell.classList.contains('up')) return;
        if (timeLeft <= 0) return;
        
        score++;
        scoreDisplay.textContent = score;
        cell.classList.remove('up'); // 叩いたらすぐに隠れる
    });
});

startButton.addEventListener('click', startGame);
