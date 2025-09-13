import numpy as np

class TicTacToeAI:
    def __init__(self):
        self.human = 'X'
        self.ai = 'O'

    def check_winner(self, board):
        # Rows & Cols
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != '':
                return board[0][i]
        # Diagonals
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]

        if '' not in board:
            return 'Draw'
        return None

    def best_move(self, board):
        best_score = -float('inf')
        move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = self.ai
                    score = self.minimax(board, 0, False, -float('inf'), float('inf'))
                    board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move if move else (None, None)

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        result = self.check_winner(board)
        if result == self.ai:
            return 1
        elif result == self.human:
            return -1
        elif result == 'Draw':
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = self.ai
                        score = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = ''
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = self.human
                        score = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = ''
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
