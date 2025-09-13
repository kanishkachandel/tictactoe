const boardDiv = document.getElementById('board');
const statusDiv = document.getElementById('status');
const playerScoreEl = document.getElementById('playerScore');
const aiScoreEl = document.getElementById('aiScore');

let playerScore = 0;
let aiScore = 0;

function createBoard(board) {
    boardDiv.innerHTML = '';
    board.forEach((row, i) => {
        row.forEach((cell, j) => {
            const div = document.createElement('div');
            div.classList.add('cell');
            div.innerText = cell;
            if (cell === '') {
                div.onclick = () => makeMove(i, j);
            }
            boardDiv.appendChild(div);
        });
    });
}

async function makeMove(row, col) {
    const res = await fetch('/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({row, col})
    });
    const data = await res.json();
    createBoard(data.board);

    if (data.winner) {
        if (data.winner === 'X') {
            playerScore++;
            playerScoreEl.innerText = playerScore;
            statusDiv.innerText = "🎉 You Win!";
            statusDiv.style.color = "green";
        } else if (data.winner === 'O') {
            aiScore++;
            aiScoreEl.innerText = aiScore;
            statusDiv.innerText = "🤖 AI Wins!";
            statusDiv.style.color = "red";
        } else {
            statusDiv.innerText = "😅 It's a Draw!";
            statusDiv.style.color = "#444";
        }
    }
}

async function restartGame() {
    const res = await fetch('/restart', {method: 'POST'});
    const data = await res.json();
    createBoard(data.board);
    statusDiv.innerText = '';
    statusDiv.style.color = "#444";
}

restartGame();
