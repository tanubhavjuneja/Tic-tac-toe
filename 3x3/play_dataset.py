import customtkinter as ctk
import pandas as pd
import random
class TicTacToeAI:
    def __init__(self, dataset_path):
        self.data = pd.read_csv(dataset_path, header=None)
        self.data.columns = [f'cell_{i}' for i in range(9)] + ['result']
    def analyze_winning_moves(self):
        move_counts = {i: 0 for i in range(9)}
        for _, row in self.data.iterrows():
            if row['result'] == 'positive':
                for i in range(9):
                    if row[f'cell_{i}'] == 'x':
                        move_counts[i] += 1
        return sorted(move_counts.items(), key=lambda x: x[1], reverse=True)
    def decide_move(self, board, difficulty):
        if difficulty == "easy":
            available_moves = [i for i in range(9) if board[i] == 'b']
            return random.choice(available_moves) if available_moves else None
        ai = 'x'
        opponent = 'o'
        for i in range(9):
            if board[i] == 'b':
                board[i] = ai
                if self.check_winner(board, ai):
                    board[i] = 'b'
                    return i
                board[i] = 'b'
        for i in range(9):
            if board[i] == 'b':
                board[i] = opponent
                if self.check_winner(board, opponent):
                    board[i] = 'b'
                    return i
                board[i] = 'b'
        self.win_moves = self.analyze_winning_moves()
        for move, _ in self.win_moves:
            if board[move] == 'b':
                return move
        return None
    def check_winner(self, board, player):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)
class TicTacToeGUI:
    def __init__(self, root, ai):
        self.root = root
        self.ai = ai
        self.difficulty = "medium"
        self.board = ['b'] * 9
        self.buttons = []
        self.root.geometry("670x800+650+100")
        self.root.configure(fg_color=("#1a1a1a"))
        self.board_frame = ctk.CTkFrame(self.root, width=650, height=650)
        self.board_frame.pack(pady=10, padx=10)
        self.create_board()
        self.control_frame = ctk.CTkFrame(self.root, width=650, height=150)
        self.control_frame.pack(pady=10, padx=10)
        self.create_controls()
    def create_board(self):
        for i in range(9):
            btn = ctk.CTkButton(self.board_frame, text="", font=("Arial", 100), width=200, height=200,
                                command=lambda i=i: self.player_move(i))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)
    def create_controls(self):
        self.status_label = ctk.CTkLabel(self.control_frame, text="Select Difficulty", font=("Arial", 50))
        self.status_label.pack(pady=5)
        difficulty_frame = ctk.CTkFrame(self.control_frame)
        difficulty_frame.pack(pady=10)
        ctk.CTkButton(difficulty_frame, text="Easy", width=200, height=50, command=lambda: self.reset_game("easy"), font=("Arial", 25)).pack(side="left", padx=5)
        ctk.CTkButton(difficulty_frame, text="Medium", width=200, height=50, command=lambda: self.reset_game("medium"), font=("Arial", 25)).pack(side="left", padx=5)
        ctk.CTkButton(difficulty_frame, text="Hard", width=200, height=50, command=lambda: self.reset_game("hard"), font=("Arial", 25)).pack(side="left", padx=5)
    def player_move(self, index):
        if self.board[index] == 'b' and not self.check_game_over():
            self.board[index] = 'o'
            self.buttons[index].configure(text="O", state="disabled")
            if self.ai.check_winner(self.board, 'o'):
                self.status_label.configure(text="You Win!")
                return
            self.status_label.configure(text="AI's Turn")
            self.disable_buttons()
            self.root.after(2000, self.ai_move)
    def ai_move(self):
        if not self.check_game_over():
            move = self.ai.decide_move(self.board, self.difficulty)
            if move is not None:
                self.board[move] = 'x'
                self.buttons[move].configure(text="X", state="disabled")
                if self.ai.check_winner(self.board, 'x'):
                    self.status_label.configure(text="AI Wins!")
                    return
                self.status_label.configure(text="Your Turn")   
            if 'b' not in self.board:
                self.status_label.configure("It's a Draw!")
        self.enable_buttons()
    def disable_buttons(self):
        for btn in self.buttons:
            btn.configure(state="disabled")
    def enable_buttons(self):
        for i, btn in enumerate(self.buttons):
            if self.board[i] == 'b':
                btn.configure(state="normal")
    def check_game_over(self):
        return self.ai.check_winner(self.board, 'x') or self.ai.check_winner(self.board, 'o') or 'b' not in self.board
    def reset_game(self, difficulty):
        self.difficulty = difficulty
        self.board = ['b'] * 9
        for btn in self.buttons:
            btn.configure(text="", state="normal")
        self.status_label.configure(text="Your Turn")
        self.first_turn()
    def first_turn(self):
        if self.difficulty == "hard":
            self.status_label.configure(text="AI's Turn")
            self.root.after(2000, self.ai_move)
        else:
            self.status_label.configure(text="Your Turn")
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Tic Tac Toe")
    ai = TicTacToeAI('dataset.csv')
    TicTacToeGUI(root, ai)
    root.mainloop()
