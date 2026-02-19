/**
 * Cyberpunk Tic-Tac-Toe Logic
 * Features: Minimax AI, Undo/Redo, Responsive Design, Keyboard Support
 */

document.addEventListener('DOMContentLoaded', () => {
    // State
    let board = Array(9).fill(null);
    let humanSymbol = 'X';
    let aiSymbol = 'O';
    let currentPlayer = 'X'; // X always starts
    let gameActive = true;
    let difficulty = 'easy';
    let moveHistory = [];
    let redoStack = [];
    
    const stats = {
        player: 0,
        ai: 0,
        draws: 0,
        totalGames: 0
    };

    // DOM Elements
    const cells = document.querySelectorAll('.cell');
    const playerWinEl = document.getElementById('player-score');
    const aiWinEl = document.getElementById('ai-score');
    const drawEl = document.getElementById('draw-score');
    const winRateEl = document.getElementById('win-rate');
    const diffBtns = document.querySelectorAll('.diff-btn');
    const symBtns = document.querySelectorAll('.sym-btn');
    const thinkingIndicator = document.getElementById('thinking-indicator');
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalMsg = document.getElementById('modal-message');
    
    // Sounds
    const sounds = {
        move: document.getElementById('sound-move'),
        win: document.getElementById('sound-win'),
        draw: document.getElementById('sound-draw'),
        hover: document.getElementById('sound-hover')
    };

    const playSound = (name) => {
        if (sounds[name]) {
            sounds[name].currentTime = 0;
            sounds[name].play().catch(e => console.log('Audio play blocked'));
        }
    };

    // Winning Combinations
    const winConditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // Cols
        [0, 4, 8], [2, 4, 6]             // Diagonals
    ];

    // Initialize Game
    const init = async () => {
    board = Array(9).fill(null);
    gameActive = true;
    currentPlayer = 'X';
    moveHistory = [];
    redoStack = [];

    cells.forEach(cell => {
        cell.className = 'cell';
        cell.innerHTML = '';
    });

    modal.classList.add('hidden');

    await fetch("http://127.0.0.1:5000/reset", { method: "POST" });

    if (currentPlayer === aiSymbol) {
        makeAiMove();
    }
};


    // Handle Cell Click
    const handleCellClick = (e) => {
        const index = e.target.dataset.index;
        
        if (board[index] || !gameActive || currentPlayer === aiSymbol) return;
        
        executeMove(index, humanSymbol);
        
        if (gameActive) {
            currentPlayer = aiSymbol;
            setTimeout(makeAiMove, 600); // Small delay for "thinking" effect
        }
    };

    const executeMove = (index, symbol) => {
        board[index] = symbol;
        const cell = cells[index];
        cell.classList.add(symbol.toLowerCase());
        
        moveHistory.push({ index, symbol });
        redoStack = []; // Clear redo on new move
        
        playSound('move');
        checkResult();
    };

    const checkResult = () => {
        let roundWon = false;
        let winningCombo = null;

        for (let condition of winConditions) {
            const [a, b, c] = condition;
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                roundWon = true;
                winningCombo = condition;
                break;
            }
        }

        if (roundWon) {
            gameActive = false;
            highlightWinner(winningCombo);
            updateStats(board[winningCombo[0]] === humanSymbol ? 'player' : 'ai');
            showGameOver(board[winningCombo[0]] === humanSymbol ? 'YOU WIN' : 'AI WINS');
            return;
        }

        if (!board.includes(null)) {
            gameActive = false;
            updateStats('draw');
            showGameOver('DRAW');
            return;
        }
    };

    const highlightWinner = (combo) => {
        combo.forEach(idx => cells[idx].classList.add('winning'));
        playSound('win');
    };

    const updateStats = (result) => {
        stats.totalGames++;
        if (result === 'player') stats.player++;
        else if (result === 'ai') stats.ai++;
        else stats.draws++;

        playerWinEl.innerText = stats.player;
        aiWinEl.innerText = stats.ai;
        drawEl.innerText = stats.draws;
        
        const rate = stats.totalGames > 0 ? Math.round((stats.player / stats.totalGames) * 100) : 0;
        winRateEl.innerText = `${rate}%`;
    };

    const showGameOver = (title) => {
        modalTitle.innerText = title;
        modalMsg.innerText = title === 'DRAW' ? "It's a stalemate in the matrix." : `${title === 'YOU WIN' ? 'Human' : 'Machine'} has dominated the arena.`;
        setTimeout(() => modal.classList.remove('hidden'), 500);
        if (title === 'DRAW') playSound('draw');
    };

    // AI Logic (Minimax)
    const makeAiMove = async () => {
    if (!gameActive) return;

    thinkingIndicator.classList.remove('hidden');

    try {
        const lastHumanMove = moveHistory[moveHistory.length - 1].index;

        const response = await fetch("http://127.0.0.1:5000/move", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ action: lastHumanMove })
        });

        const data = await response.json();
        console.log("SERVER RESPONSE:", data); // ⭐ DEBUG

        thinkingIndicator.classList.add('hidden');

        if (data.error) {
            alert("Server error: " + data.error);
            return;
        }

        if (data.ai_action !== undefined) {
            executeMove(data.ai_action, aiSymbol);
        }

        if (data.done) gameActive = false;
        else currentPlayer = humanSymbol;

    } catch (err) {
        thinkingIndicator.classList.add('hidden');
        console.error(err);
        alert("Connection error");
    }
};



    const getRandomMove = () => {
        const available = board.map((v, i) => v === null ? i : null).filter(v => v !== null);
        return available[Math.floor(Math.random() * available.length)];
    };

    const minimax = (newBoard, player) => {
        const availSpots = newBoard.map((v, i) => v === null ? i : null).filter(v => v !== null);

        if (checkWin(newBoard, humanSymbol)) return { score: -10 };
        if (checkWin(newBoard, aiSymbol)) return { score: 10 };
        if (availSpots.length === 0) return { score: 0 };

        const moves = [];
        for (let i = 0; i < availSpots.length; i++) {
            const move = {};
            move.index = availSpots[i];
            newBoard[availSpots[i]] = player;

            if (player === aiSymbol) {
                move.score = minimax(newBoard, humanSymbol).score;
            } else {
                move.score = minimax(newBoard, aiSymbol).score;
            }

            newBoard[availSpots[i]] = null;
            moves.push(move);
        }

        let bestMove;
        if (player === aiSymbol) {
            let bestScore = -10000;
            for (let i = 0; i < moves.length; i++) {
                if (moves[i].score > bestScore) {
                    bestScore = moves[i].score;
                    bestMove = i;
                }
            }
        } else {
            let bestScore = 10000;
            for (let i = 0; i < moves.length; i++) {
                if (moves[i].score < bestScore) {
                    bestScore = moves[i].score;
                    bestMove = i;
                }
            }
        }
        return moves[bestMove];
    };

    const checkWin = (b, p) => {
        return winConditions.some(c => b[c[0]] === p && b[c[1]] === p && b[c[2]] === p);
    };

    // Undo / Redo
    const undo = () => {
        if (moveHistory.length < 1 || !gameActive || currentPlayer === aiSymbol) return;
        
        // Undo AI move and Player move
        for(let i=0; i<2; i++) {
            if (moveHistory.length > 0) {
                const lastMove = moveHistory.pop();
                redoStack.push(lastMove);
                board[lastMove.index] = null;
                const cell = cells[lastMove.index];
                cell.className = 'cell';
                cell.innerHTML = '';
            }
        }
        currentPlayer = humanSymbol;
    };

    const redo = () => {
        if (redoStack.length < 1 || !gameActive || currentPlayer === aiSymbol) return;
        
        // Redo Player move then AI move
        for(let i=0; i<2; i++) {
            if (redoStack.length > 0) {
                const nextMove = redoStack.pop();
                board[nextMove.index] = nextMove.symbol;
                const cell = cells[nextMove.index];
                cell.classList.add(nextMove.symbol.toLowerCase());
                moveHistory.push(nextMove);
            }
        }
    };

    // Event Listeners
    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
        cell.addEventListener('mouseenter', () => playSound('hover'));
    });

    diffBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            diffBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            difficulty = btn.dataset.diff;
        });
    });

    symBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (moveHistory.length > 0) return; // Can't change during game
            symBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            humanSymbol = btn.dataset.sym;
            aiSymbol = humanSymbol === 'X' ? 'O' : 'X';
            init();
        });
    });

    document.getElementById('reset-btn').addEventListener('click', () => {
        stats.player = 0;
        stats.ai = 0;
        stats.draws = 0;
        stats.totalGames = 0;
        updateStats();
        init();
    });

    document.getElementById('new-game-btn').addEventListener('click', init);
    document.getElementById('play-again-btn').addEventListener('click', init);
    document.getElementById('undo-btn').addEventListener('click', undo);
    document.getElementById('redo-btn').addEventListener('click', redo);

    // Keyboard Support
    let focusedIndex = 0;
    document.addEventListener('keydown', (e) => {
        if (modal.classList.contains('hidden')) {
            if (e.key === 'ArrowRight' && focusedIndex < 8) focusedIndex++;
            if (e.key === 'ArrowLeft' && focusedIndex > 0) focusedIndex--;
            if (e.key === 'ArrowDown' && focusedIndex < 6) focusedIndex += 3;
            if (e.key === 'ArrowUp' && focusedIndex > 2) focusedIndex -= 3;
            
            cells.forEach(c => c.style.boxShadow = '');
            cells[focusedIndex].style.boxShadow = '0 0 15px var(--neon-blue)';
            
            if (e.key === 'Enter') cells[focusedIndex].click();
        } else {
            if (e.key === 'Escape') modal.classList.add('hidden');
            if (e.key === 'Enter') init();
        }
    });
 const controller = new AbortController();

setTimeout(() => controller.abort(), 5000);

    init();
});
