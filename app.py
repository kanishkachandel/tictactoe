from flask import Flask, render_template, request, jsonify
from tic_tac_toe_ai import TicTacToeAI
import numpy as np

app = Flask(__name__)
ai = TicTacToeAI()

# Global game board
board = np.full((3, 3), '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global board
    data = request.get_json()
    row, col = data['row'], data['col']

    # Player move
    if board[row][col] == '':
        board[row][col] = 'X'

        # Check winner
        winner = ai.check_winner(board)
        if winner:
            return jsonify({'board': board.tolist(), 'winner': winner})

        # AI move
        ai_row, ai_col = ai.best_move(board)
        if ai_row is not None:
            board[ai_row][ai_col] = 'O'

        # Check winner after AI
        winner = ai.check_winner(board)
        if winner:
            return jsonify({'board': board.tolist(), 'winner': winner})

    # Draw check
    if '' not in board:
        return jsonify({'board': board.tolist(), 'winner': 'Draw'})

    return jsonify({'board': board.tolist(), 'winner': None})

@app.route('/restart', methods=['POST'])
def restart():
    global board
    board = np.full((3, 3), '')
    return jsonify({'board': board.tolist(), 'winner': None})

if __name__ == '__main__':
    app.run(debug=True)
