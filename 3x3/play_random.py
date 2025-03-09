import customtkinter as ctk
import random
class TicTacToeAI:
    def __init__(self):
        self.win_conditions = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]
    def decide_move(self, board):
        available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == 'b']
        if available_moves:
            return random.choice(available_moves)
        return None
    def check_winner(self, board, player):
        return any(all(board[r][c] == player for r, c in condition) for condition in self.win_conditions)
class TicTacToeGUI:
    def __init__(self, root, ai):
        self.root = root
        self.ai = ai
        self.board = [['b'] * 3 for _ in range(3)]
        self.buttons = {}
        self.root.geometry("670x800+650+100")
        self.root.configure(fg_color=("white"))
        self.root.overrideredirect(True)
        self.board_frame = ctk.CTkFrame(self.root, width=650, height=650, fg_color="white")
        self.board_frame.pack(pady=10, padx=10)
        self.create_board()
        self.control_frame = ctk.CTkFrame(self.root, width=650, height=150, fg_color="white")
        self.control_frame.pack(pady=10, padx=10)
        self.create_controls()
    def create_board(self):
        for r in range(3):
            for c in range(3):
                btn = ctk.CTkButton(self.board_frame, text="", font=("Arial", 160), width=200, height=200,
                                    command=lambda r=r, c=c: self.player_move(r, c), text_color="white",
                                    fg_color="#3bc8f4" if (r+c) % 2 == 0 else "#2a88c8", text_color_disabled="white", hover=False)
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[(r, c)] = btn
    def create_controls(self):
        self.status_label = ctk.CTkLabel(self.control_frame, text="Your Turn", font=("Arial", 50), text_color="#2a88c8")
        self.status_label.pack(pady=5)
        self.reset_button = ctk.CTkButton(self.control_frame, text="Reset", width=400, height=50,
                                         command=self.reset_game, font=("Arial", 25), fg_color="#3bc8f4",
                                         text_color="white", hover=False)
        self.reset_button.pack(side="left", padx=5)
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
                    self.buttons[(r, c)].configure(state="normal")
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
        self.status_label.configure(text="Your Turn")
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Tic Tac Toe")
    ai = TicTacToeAI()
    TicTacToeGUI(root, ai)
    root.mainloop()