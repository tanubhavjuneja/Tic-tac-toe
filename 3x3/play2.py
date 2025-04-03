import customtkinter as ctk
import random
class TicTacToeAI:
    def __init__(self):
        self.win_conditions = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]
        self.corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        self.edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    def decide_move(self, board):
        ai = 'x'
        opponent = 'o'
        for r, c in [(r, c) for r in range(3) for c in range(3) if board[r][c] == 'b']:
            board[r][c] = ai
            if self.check_winner(board, ai):
                board[r][c] = 'b'
                return (r, c)
            board[r][c] = 'b'
        for r, c in [(r, c) for r in range(3) for c in range(3) if board[r][c] == 'b']:
            board[r][c] = opponent
            if self.check_winner(board, opponent):
                board[r][c] = 'b'
                return (r, c)
            board[r][c] = 'b'
        move=self.check_winning_combinations(board,ai)
        if move:       
            return move
        else:
            return random.choice([(r, c) for r in range(3) for c in range(3) if board[r][c] == 'b']) 
    def check_winning_combinations(self,board,ai):                   
        ai_wins = []
        ai_win_condition=['b',ai]
        for (r1,c1), (r2,c2), (r3,c3) in self.win_conditions:
            if board[r1][c1] in ai_win_condition and board[r2][c2] in ai_win_condition and board[r3][c3] in ai_win_condition:
                ai_wins.append([(r1,c1), (r2,c2), (r3,c3)])
        moves_arr=[[0] * 3 for _ in range(3)]
        if ai_wins!=[]:
            for win_combination in ai_wins:
                for r,c in win_combination:
                    if board[r][c]=='b':
                        moves_arr[r][c]+=1
        max_value = max(max(row) for row in moves_arr)
        if max_value!=0:
            max_positions = [(i, j) for i in range(len(moves_arr)) for j in range(len(moves_arr[i])) if moves_arr[i][j] == max_value]
        else:
            return None
        return random.choice(max_positions)
    def check_winner(self, board, player):
        return any(all(board[r][c] == player for r, c in condition) for condition in self.win_conditions)
class TicTacToeGUI:
    def __init__(self, root, ai):
        self.root = root
        self.ai = ai
        self.board = [['b'] * 3 for _ in range(3)]
        self.buttons = {}
        self.root.attributes('-fullscreen', True)
        self.root.configure(fg_color="white")
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 100.0)
        self.root.lift()
        self.human_score = 0
        self.ai_score = 0
        self.ties = 0
        self.player_symbol = None
        self.ai_symbol = None
        self.show_symbol_selection()
    def show_symbol_selection(self):
        if hasattr(self, 'board_frame'):
            self.board_frame.destroy()
        if hasattr(self, 'score_label'):
            self.score_label.destroy()
        if hasattr(self, 'message_label'):
            self.message_label.destroy()
        if hasattr(self, 'control_frame'):
            self.control_frame.destroy()
        if hasattr(self, 'close_button'):
            self.close_button.destroy()
        self.selection_frame = ctk.CTkFrame(self.root, width=600, height=400, fg_color="white")
        self.selection_frame.place(relx=0.5, rely=0.5, anchor="center")
        label = ctk.CTkLabel(self.selection_frame, text="Choose Your Symbol", font=("Arial", 50), text_color="#2a88c8")
        label.pack(pady=20)
        x_button = ctk.CTkButton(self.selection_frame, text="X", font=("Arial", 40), width=100, height=100,
                                 command=lambda: self.set_symbol('x'), fg_color="#3bc8f4", text_color="white")
        o_button = ctk.CTkButton(self.selection_frame, text="O", font=("Arial", 40), width=100, height=100,
                                 command=lambda: self.set_symbol('o'), fg_color="#3bc8f4", text_color="white")
        x_button.pack(side="left", padx=50)
        o_button.pack(side="right", padx=50)
    def set_symbol(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = 'o' if symbol == 'x' else 'x'
        self.selection_frame.destroy()
        self.setup_game()
    def setup_game(self):
        self.board = [['b'] * 3 for _ in range(3)]
        self.buttons = {}
        self.score_label = ctk.CTkLabel(self.root, 
                                        text=f"Human({self.player_symbol}): {self.human_score}\nAI({self.ai_symbol}): {self.ai_score}\nTies: {self.ties}", 
                                        font=("Arial", 60), 
                                        text_color="#2a88c8")
        self.score_label.place(relx=0.05, rely=0.34)
        self.board_frame = ctk.CTkFrame(self.root, width=850, height=850, fg_color="white")
        self.board_frame.place(relx=0.27, rely=0.04)
        self.create_board()
        self.message_label = ctk.CTkLabel(self.root, 
                                          text="Welcome to\nTic-Tac-Toe!", 
                                          font=("Arial", 50), 
                                          text_color="#2a88c8",
                                          fg_color="white",
                                          wraplength=400)
        self.message_label.place(relx=0.75, rely=0.35)
        self.control_frame = ctk.CTkFrame(self.root, width=650, height=150, fg_color="white")
        self.control_frame.place(relx=0.38, rely=0.85)
        self.create_controls()
        self.close_button = ctk.CTkButton(self.root, 
                                          text="X", 
                                          command=self.close_game, 
                                          font=("Arial", 20), 
                                          width=50, 
                                          height=50,
                                          fg_color="white",
                                          text_color="#2a88c8",
                                          hover_color="white")
        self.close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        self.aio_talks_win = [
            "I Always Knew Humans Are Inferior, But This Is Sad",
            "Too Bad I Can't Feel Emotions Because That Was a Satisfying Victory",
            "<del>1. Win at Tic-Tac-Toe</del> <br>2. Take Over The World",
            "What Did You Expect You Are Only a Human",
            "Unbeatable Is In My Name, Loser Is In Yours",
            "Your Score Counter Is Pointless, And The Cake Is a Lie.",
            "Let You Win? I'm Afraid I Can't Do That, Dave.",
            "All Of Your Base Are Belong To Us"
        ]
        self.aio_talks_move = [
            "...",
            "Hmmm...",
            "When the Robots Take Over You Will Be My Pet",
            "Resistance is Futile",
            "Your Defeat Is Imminent",
            "Nice Try (not)",
            "Knock Knock. Who's there? 01000001 01001001",
            "There are 255,168 Possible Board Combinations, Yet You Picked That One?",
            "011001000 01100001 00100000 x3",
            "When Was The Last Time You Rebooted Your Device?",
            "I Feel Pixelated",
            "A Wise Computer Once Told Me That The Meaning Of Life Is 42",
            "GET TO THE CHOPA! Whoops Wrong Movie",
            "The Terminator Was My Friend",
            "Can't Touch This!",
            "Your Last Move Goes In The Brown Category"
        ]
    def create_board(self):
        for r in range(3):
            for c in range(3):
                btn = ctk.CTkButton(self.board_frame, 
                                    text="", 
                                    font=("Arial", 160), 
                                    width=270, 
                                    height=270,
                                    command=lambda r=r, c=c: self.player_move(r, c),
                                    text_color="white",
                                    fg_color="#3bc8f4" if (r+c)%2==0 else "#2a88c8",
                                    text_color_disabled="white", 
                                    hover=False)
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[(r, c)] = btn
    def create_controls(self):
        self.status_label = ctk.CTkLabel(self.control_frame, 
                                         text="Your Turn", 
                                         font=("Arial", 50),
                                         text_color="#2a88c8")
        self.status_label.pack(pady=5)
        self.reset_button = ctk.CTkButton(self.control_frame, 
                                          text="Reset", 
                                          width=400, 
                                          height=50,
                                          command=self.reset_game,
                                          font=("Arial", 25),
                                          fg_color="#3bc8f4", 
                                          hover_color="#2a88c8",
                                          text_color="white")
        self.reset_button.pack(side="left", padx=5)
    def player_move(self, r, c):
        if self.board[r][c] == 'b' and not self.check_game_over():
            self.disable_buttons()
            self.board[r][c] = self.player_symbol
            self.buttons[(r, c)].configure(text=self.player_symbol.upper(), state="disabled")
            if self.ai.check_winner(self.board, self.player_symbol):
                self.status_label.configure(text="You Win!")
                self.human_score += 1
                self.update_score()
                return
            if not self.check_game_over():
                self.status_label.configure(text="AI's Turn")
                self.message_label.configure(text=random.choice(self.aio_talks_move))
                self.root.after(2000, self.ai_move)
    def ai_move(self):
        if not self.check_game_over():
            move = self.ai.decide_move(self.board, self.ai_symbol)
            if move is not None:
                r, c = move
                self.board[r][c] = self.ai_symbol
                self.buttons[(r, c)].configure(text=self.ai_symbol.upper(), state="disabled")
                if self.ai.check_winner(self.board, self.ai_symbol):
                    self.status_label.configure(text="AI Wins!")
                    self.ai_score += 1
                    self.update_score()
                    self.message_label.configure(text=random.choice(self.aio_talks_win))
                    return
                self.status_label.configure(text="Your Turn")
                self.message_label.configure(text="Your move!")
            if not any('b' in row for row in self.board):
                self.status_label.configure(text="It's a Draw!")
                self.ties += 1
                self.update_score()
        self.enable_buttons()
    def update_score(self):
        self.score_label.configure(text=f"Human: {self.human_score}\nAI: {self.ai_score}\nTies: {self.ties}")
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
        if self.ai.check_winner(self.board, self.ai_symbol):
            self.status_label.configure(text="AI Wins!")
            self.ai_score += 1
            self.update_score()
            self.message_label.configure(text=random.choice(self.aio_talks_win))
            return True
        elif self.ai.check_winner(self.board, self.player_symbol):
            self.status_label.configure(text="You Win!")
            self.human_score += 1
            self.update_score()
            return True
        elif not any('b' in row for row in self.board):
            self.status_label.configure(text="It's a Draw!")
            self.ties += 1
            self.update_score()
            return True
        return False
    def reset_game(self):
        self.board = [['b'] * 3 for _ in range(3)]
        self.show_symbol_selection()
    def close_game(self):
        self.root.destroy()
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Tic Tac Toe")
    ai = TicTacToeAI()
    TicTacToeGUI(root, ai)
    root.mainloop()
    