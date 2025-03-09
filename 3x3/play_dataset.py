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
        self.board = [['b'] * 3 for _ in range(3)]
        self.buttons = {}
        self.root.geometry("670x800+650+100")
        self.root.configure(fg_color=("white"))
        self.root.overrideredirect(True)
        self.board_frame = ctk.CTkFrame(self.root, width=650, height=650,fg_color="white")
        self.board_frame.pack(pady=10, padx=10)
        self.create_board() 
        self.control_frame = ctk.CTkFrame(self.root, width=650, height=150,fg_color="white")
        self.control_frame.pack(pady=10, padx=10)
        self.create_controls()
    def create_board(self):
        for r in range(3):
            for c in range(3):
                btn = ctk.CTkButton(self.board_frame, text="", font=("Arial", 160), width=200, height=200,
                                    command=lambda r=r, c=c: self.player_move(r, c),text_color="white",fg_color="#3bc8f4" if (r+c)%2==0 else "#2a88c8", hover=False,text_color_disabled="white")
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[(r, c)] = btn
    def create_controls(self):
        self.status_label = ctk.CTkLabel(self.control_frame, text="Your Turn", font=("Arial", 50),text_color="#2a88c8")
        self.status_label.pack(pady=5)
        self.reset_button =ctk.CTkButton(self.control_frame, text="Reset", width=400, height=50,command=self.reset_game,font=("Arial", 25), hover=False,fg_color="#3bc8f4",text_color="white").pack(side="left", padx=5)
    def player_move(self, r, c):
        if self.board[r][c] == 'b' and not self.check_game_over():
            self.disable_buttons()
            self.board[r][c] = 'o'
            self.buttons[(r, c)].configure(text="O", state="disabled")
            if self.ai.check_winner(self.board, 'o'):
                self.status_label.configure(text="You Win!")
                return
            if not self.check_game_over():
                self.status_label.configure(text="AI's Turn")
                self.root.after(2000, self.ai_move)
    def ai_move(self):
        if not self.check_game_over():
            move = self.ai.decide_move(self.board)
            if move is not None:
                r, c = move
                self.board[r][c] = 'x'
                self.buttons[(r, c)].configure(text="X", state="disabled")
                if self.ai.check_winner(self.board, 'x'):
                    self.status_label.configure(text="AI Wins!")
                    return
                self.status_label.configure(text="Your Turn")
            if not any('b' in row for row in self.board):
                self.status_label.configure(text="It's a Draw!")
        self.enable_buttons()
    def disable_buttons(self):
        for r in range(3):
            for c in range(3):
                self.buttons[(r, c)].configure(state="disabled")
    def enable_buttons(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 'b':  
                    self.buttons[(r,c)].configure(state="normal")
    def check_game_over(self):
        if self.ai.check_winner(self.board, 'x'):
            self.status_label.configure(text="AI Wins!")
            return True
        elif self.ai.check_winner(self.board, 'o'):
            self.status_label.configure(text="You Win!")
            return True
        elif not any('b' in row for row in self.board):
            self.status_label.configure(text="It's a Draw!")
            return True
        return False
    def reset_game(self):
        self.board = [['b'] * 3 for _ in range(3)]
        for (r, c), btn in self.buttons.items():
            btn.configure(text="", state="normal")
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Tic Tac Toe")
    ai = TicTacToeAI('dataset.csv')
    TicTacToeGUI(root, ai)
    root.mainloop()
