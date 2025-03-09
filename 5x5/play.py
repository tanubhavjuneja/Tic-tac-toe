import customtkinter as ctk
import random
class RandomAI:
    def __init__(self):
        self.win_conditions = [
            [(r, c), (r, c + 1), (r, c + 2)] for r in range(5) for c in range(3)
        ] + [
            [(r, c), (r + 1, c), (r + 2, c)] for c in range(5) for r in range(3)
        ] + [
            [(r, c), (r + 1, c + 1), (r + 2, c + 2)] for r in range(3) for c in range(3)
        ] + [
            [(r, c), (r + 1, c - 1), (r + 2, c - 2)] for r in range(3) for c in range(2, 5)
        ]
    def play_game(self, board):
        ai = 'X'
        opponent = 'O'
        for move in [(r, c) for r in range(5) for c in range(5) if board[r][c] == 'b']:
            board[move[0]][move[1]] = ai
            if self.check_winner(board, ai):
                board[move[0]][move[1]] = 'b'
                return move
            board[move[0]][move[1]] = 'b'
        for move in [(r, c) for r in range(5) for c in range(5) if board[r][c] == 'b']:
            board[move[0]][move[1]] = opponent
            if self.check_winner(board, opponent):
                board[move[0]][move[1]] = 'b'
                return move
            board[move[0]][move[1]] = 'b'
        return random.choice([(r, c) for r in range(5) for c in range(5) if board[r][c] == 'b'])
    def check_winner(self, board, player):
        return any(all(board[r][c] == player for r, c in condition) for condition in self.win_conditions)
import random

class SmartAI:
    def __init__(self):
        self.win_conditions = [
            [(r, c), (r, c + 1), (r, c + 2)] for r in range(5) for c in range(3)
        ] + [
            [(r, c), (r + 1, c), (r + 2, c)] for c in range(5) for r in range(3)
        ] + [
            [(r, c), (r + 1, c + 1), (r + 2, c + 2)] for r in range(3) for c in range(3)
        ] + [
            [(r, c), (r + 1, c - 1), (r + 2, c - 2)] for r in range(3) for c in range(2, 5)
        ]

    def play_game(self, board):
        best_move = None
        best_score = float('-inf')

        for move in [(r, c) for r in range(5) for c in range(5) if board[r][c] == 'b']:
            board[move[0]][move[1]] = 'X'
            score = self.minimax(board, 0, False, float('-inf'), float('inf'))
            board[move[0]][move[1]] = 'b'

            if score > best_score:
                best_score = score
                best_move = move

        return best_move if best_move else random.choice([(r, c) for r in range(5) for c in range(5) if board[r][c] == 'b'])

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner(board, 'X'):
            return 10 - depth  # AI wins
        if self.check_winner(board, 'O'):
            return depth - 10  # Opponent wins
        if all(cell != 'b' for row in board for cell in row):
            return 0  # Draw

        if is_maximizing:
            max_eval = float('-inf')
            for move in [(r, c) for r in range(5) for c in range(5) if board[r][c] == 'b']:
                print("yes")
                board[move[0]][move[1]] = 'X'
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                board[move[0]][move[1]] = 'b'
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in [(r, c) for r in range(5) for c in range(5) if board[r][c] == 'b']:
                print("yes")
                board[move[0]][move[1]] = 'O'
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                board[move[0]][move[1]] = 'b'
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def check_winner(self, board, player):
        return any(all(board[r][c] == player for r, c in condition) for condition in self.win_conditions)

class TicTacToeGUI:
    def __init__(self, root, ai1, ai2):
        self.root = root
        self.ai1 = ai1
        self.ai2 = ai2
        self.board = [['b'] * 5 for _ in range(5)]
        self.buttons = {}
        self.current_player = 'X'
        self.root.geometry("850x1000+500+50")
        self.root.configure(fg_color=("#1a1a1a"))
        self.board_frame = ctk.CTkFrame(self.root, width=850, height=850)
        self.board_frame.pack(pady=10, padx=10)
        self.create_board()
        self.status_label = ctk.CTkLabel(self.root, text="AI 1's Turn", font=("Arial", 50))
        self.status_label.pack(pady=5)
        self.root.after(1000, self.play_game)
    def create_board(self):
        for r in range(5):
            for c in range(5):
                btn = ctk.CTkButton(self.board_frame, text="", font=("Arial", 50), width=150, height=150)
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[(r, c)] = btn
    def play_game(self):
        if any('b' in row for row in self.board):
            ai = self.ai1 if self.current_player == 'X' else self.ai2
            move = ai.play_game(self.board)
            if move is not None:
                r, c = move
                if self.board[r][c]=='b':
                    self.board[r][c] = self.current_player
                    self.buttons[(r, c)].configure(text=self.current_player)
                else:
                    print("Invalid Move")
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                    self.status_label.configure(text=f"{self.current_player} Wins!")
                if self.check_winner(self.board, self.current_player):
                    self.status_label.configure(text=f"{self.current_player} Wins!")
                    return
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_label.configure(text=f"{self.current_player}'s Turn")
                self.root.after(1000, self.play_game)
    def check_winner(self, board, player):
        win_conditions = [
            [(r, c), (r, c + 1), (r, c + 2)] for r in range(5) for c in range(3)
        ] + [
            [(r, c), (r + 1, c), (r + 2, c)] for c in range(5) for r in range(3)
        ] + [
            [(r, c), (r + 1, c + 1), (r + 2, c + 2)] for r in range(3) for c in range(3)
        ] + [
            [(r, c), (r + 1, c - 1), (r + 2, c - 2)] for r in range(3) for c in range(2, 5)
        ]
        return any(all(board[r][c] == player for r, c in condition) for condition in win_conditions)
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Tic Tac Toe - AI vs AI")
    ai1 = RandomAI()
    ai2 = SmartAI()
    TicTacToeGUI(root, ai1, ai2)
    root.mainloop()