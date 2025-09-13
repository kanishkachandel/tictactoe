import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Tic Tac Toe AI", page_icon="🎮", layout="centered")

st.title("🤖 Tic Tac Toe with AI")
st.write("Play against an unbeatable AI (Minimax algorithm). Good luck! 😉")

# --- Initialize game state ---
if "board" not in st.session_state:
    st.session_state.board = np.full((3,3), "", dtype=str)
    st.session_state.turn = "X"  # Player always X
    st.session_state.game_over = False
    st.session_state.winner = None

# --- Helper: Check Winner ---
def check_winner(board):
    for i in range(3):
        if board[i,0] == board[i,1] == board[i,2] != "":
            return board[i,0]
        if board[0,i] == board[1,i] == board[2,i] != "":
            return board[0,i]
    if board[0,0] == board[1,1] == board[2,2] != "":
        return board[0,0]
    if board[0,2] == board[1,1] == board[2,0] != "":
        return board[0,2]
    return None

# --- Helper: Minimax AI ---
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif "" not in board:
        return 0

    if is_maximizing:
        best_score = -999
        for i in range(3):
            for j in range(3):
                if board[i,j] == "":
                    board[i,j] = "O"
                    score = minimax(board, depth+1, False)
                    board[i,j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 999
        for i in range(3):
            for j in range(3):
                if board[i,j] == "":
                    board[i,j] = "X"
                    score = minimax(board, depth+1, True)
                    board[i,j] = ""
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -999
    move = None
    for i in range(3):
        for j in range(3):
            if board[i,j] == "":
                board[i,j] = "O"
                score = minimax(board, 0, False)
                board[i,j] = ""
                if score > best_score:
                    best_score = score
                    move = (i,j)
    return move

# --- Game Board UI ---
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if st.session_state.board[i,j] == "" and not st.session_state.game_over:
            if cols[j].button(" ", key=f"{i}{j}", use_container_width=True, height=100):
                st.session_state.board[i,j] = "X"
                st.session_state.turn = "O"
        else:
            cols[j].button(st.session_state.board[i,j], key=f"{i}{j}", disabled=True, use_container_width=True, height=100)

# --- AI Move ---
if st.session_state.turn == "O" and not st.session_state.game_over:
    move = best_move(st.session_state.board)
    if move:
        st.session_state.board[move] = "O"
    st.session_state.turn = "X"

# --- Check Winner ---
winner = check_winner(st.session_state.board)
if winner:
    st.session_state.game_over = True
    st.session_state.winner = winner
    st.success(f"🎉 {winner} wins!")
elif "" not in st.session_state.board:
    st.session_state.game_over = True
    st.info("😅 It's a draw!")

# --- Restart Button ---
if st.button("🔄 Restart Game"):
    st.session_state.board = np.full((3,3), "", dtype=str)
    st.session_state.turn = "X"
    st.session_state.game_over = False
    st.session_state.winner = None
