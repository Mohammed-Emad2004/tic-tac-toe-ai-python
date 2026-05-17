import tkinter as tk
from tkinter import messagebox
import math

# Tic Tac Toe AI - Minimax

PLAYER = "X"
AI = "O"

# Difficulty Levels باستخدام الـ Depth
DIFFICULTY = {
    "Easy": 1,
    "Medium": 3,
    "Hard": 9
}

current_depth = DIFFICULTY["Medium"]

# Game Board
board = [" " for _ in range(9)]

# GUI Setup

root = tk.Tk()
root.title("Tic Tac Toe - Minimax AI")
root.geometry("420x720")
root.configure(bg="#1e1e1e")

# Title

title = tk.Label(
    root,
    text="Tic Tac Toe AI",
    font=("Arial", 28, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(pady=15)

# Difficulty Label

difficulty_label = tk.Label(
    root,
    text="Difficulty: Medium",
    font=("Arial", 15, "bold"),
    bg="#1e1e1e",
    fg="white"
)

difficulty_label.pack(pady=10)

# Difficulty Buttons

difficulty_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

difficulty_frame.pack(pady=5)


def set_difficulty(level):

    global current_depth

    current_depth = DIFFICULTY[level]

    difficulty_label.config(
        text=f"Difficulty: {level}"
    )


for level in DIFFICULTY:

    btn = tk.Button(
        difficulty_frame,
        text=level,
        font=("Arial", 12, "bold"),
        width=10,
        bg="#2d3436",
        fg="white",
        activebackground="#636e72",
        command=lambda l=level: set_difficulty(l)
    )

    btn.pack(
        side="left",
        padx=5
    )

# Board Frame

buttons_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

buttons_frame.pack(pady=20)

buttons = []

# Check Winner

def check_winner(bd, player):

    winning_positions = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for pos in winning_positions:

        if all(bd[i] == player for i in pos):
            return True

    return False

# Draw Check

def is_draw(bd):

    return " " not in bd

# Minimax Algorithm

def minimax(bd, depth, is_maximizing, max_depth):

    # AI Wins
    if check_winner(bd, AI):
        return 1

    # Player Wins
    if check_winner(bd, PLAYER):
        return -1

    # Draw
    if is_draw(bd):
        return 0

    # Depth Limit
    if depth >= max_depth:
        return 0

    # Maximizing Player (AI)
    if is_maximizing:

        best_score = -math.inf

        for i in range(9):

            if bd[i] == " ":

                bd[i] = AI

                score = minimax(
                    bd,
                    depth + 1,
                    False,
                    max_depth
                )

                bd[i] = " "

                best_score = max(score, best_score)

        return best_score

    # Minimizing Player (Human)
    else:

        best_score = math.inf

        for i in range(9):

            if bd[i] == " ":

                bd[i] = PLAYER

                score = minimax(
                    bd,
                    depth + 1,
                    True,
                    max_depth
                )

                bd[i] = " "

                best_score = min(score, best_score)

        return best_score

# AI Move

def ai_move():

    best_score = -math.inf
    best_move = None

    for i in range(9):

        if board[i] == " ":

            board[i] = AI

            score = minimax(
                board,
                0,
                False,
                current_depth
            )

            board[i] = " "

            if score > best_score:

                best_score = score
                best_move = i

    if best_move is not None:

        board[best_move] = AI

        buttons[best_move].config(
            text=AI,
            fg="#ff7675"
        )

    check_game_over()

# Disable Buttons

def disable_buttons():

    for btn in buttons:
        btn.config(state="disabled")

# Check Game Over

def check_game_over():

    if check_winner(board, PLAYER):

        messagebox.showinfo(
            "Game Over",
            "You Win!"
        )

        disable_buttons()
        return

    if check_winner(board, AI):

        messagebox.showinfo(
            "Game Over",
            "AI Wins!"
        )

        disable_buttons()
        return

    if is_draw(board):

        messagebox.showinfo(
            "Game Over",
            "Draw!"
        )

        disable_buttons()

# Player Move

def player_move(index):

    if board[index] == " ":

        board[index] = PLAYER

        buttons[index].config(
            text=PLAYER,
            fg="#74b9ff"
        )

        check_game_over()

        if not check_winner(board, PLAYER) and not is_draw(board):

            ai_move()

# Restart Game

def restart_game():

    global board

    board = [" " for _ in range(9)]

    for btn in buttons:

        btn.config(
            text="",
            state="normal"
        )

# Create Board Buttons

for i in range(9):

    btn = tk.Button(
        buttons_frame,
        text="",
        font=("Arial", 30, "bold"),
        width=5,
        height=2,
        bg="#2d3436",
        fg="white",
        activebackground="#636e72",
        command=lambda i=i: player_move(i)
    )

    btn.grid(
        row=i // 3,
        column=i % 3,
        padx=5,
        pady=5
    )

    buttons.append(btn)

# Restart Button

restart_button = tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 16, "bold"),
    width=18,
    height=2,
    bg="#00b894",
    fg="white",
    activebackground="#55efc4",
    command=restart_game
)

restart_button.pack(pady=25)

# Run Program
root.mainloop()