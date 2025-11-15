from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, HTMLResponse
import random
import uvicorn
from pathlib import Path
import requests
import threading
class TicTacToeAI:
    def __init__(self):
        self.win_conditions = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]
        self.corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        self.edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    def decide_move(self, board,ai):
        if ai=='x':
            opponent = 'o' 
        else:
            opponent='x'
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
        move=self.check_winning_combinations(board,ai,opponent)
        if move:       
            return move
        else:
            return random.choice([(r, c) for r in range(3) for c in range(3) if board[r][c] == 'b']) 
    def check_winning_combinations(self,board,ai,opponent):
        num_moves = sum(1 for row in board for cell in row if cell != 'b')
        if num_moves == 1:
            self.opponent_center=None
            if board[1][1] == 'b':
                return (1,1)
            else:
                self.opponent_center=(1,1)
        if num_moves == 3:
            check_move=0
            opponent_corner=None
            opponent_edge=None
            for r,c in self.corners:
                if board[r][c] == opponent:
                    if opponent_corner==None:
                        opponent_corner=(r,c)
                    else:
                        check_move=r+c+opponent_corner[0]+opponent_corner[1]
            if check_move==4:
                for edge in self.edges:
                    if board[edge[0]][edge[1]] == 'b':
                        return edge
            if self.opponent_center and opponent_corner:
                for r,c in self.corners:
                    if board[r][c] == 'b':
                        return (r,c)
            for r,c in self.edges:
                if board[r][c] != 'b':
                    if opponent_edge==None:
                        opponent_edge=(r,c)
                    else:
                        if max(abs(opponent_edge[0]-r),abs(opponent_edge[1]-c)) == 1:
                            if r==1:
                                return (opponent_edge[0],c)
                            else:
                                return (r,opponent_edge[1])
            if opponent_corner and opponent_edge:
                if opponent_edge[0]==1:
                    return (opponent_corner[0],opponent_edge[1])
                else:
                    return (opponent_edge[0],opponent_corner[1])
        ai_wins = []
        opponent_wins = []
        ai_win_condition=['b',ai]
        opponent_win_condition=['b',opponent]
        for (r1,c1), (r2,c2), (r3,c3) in self.win_conditions:
            if board[r1][c1] in ai_win_condition and board[r2][c2] in ai_win_condition and board[r3][c3] in ai_win_condition:
                ai_wins.append([(r1,c1), (r2,c2), (r3,c3)])
            elif board[r1][c1] in opponent_win_condition and board[r2][c2] in opponent_win_condition and board[r3][c3] in opponent_win_condition:
                opponent_wins.append([(r1,c1), (r2,c2), (r3,c3)])
        moves_arr=[[0] * 3 for _ in range(3)]
        if ai_wins!=[]:
            for win_combination in ai_wins:
                for r,c in win_combination:
                    if board[r][c]=='b':
                        moves_arr[r][c]+=1
        if opponent_wins!=[]:
            for win_combination in opponent_wins:
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
app = FastAPI()
ai_engine = TicTacToeAI()
board = [['b'] * 3 for _ in range(3)]   
player_symbol = None            
ai_symbol = None
scores = {"human": 0, "ai": 0, "ties": 0}
game_over = False
last_message = "Choose your symbol to start."
ai_talks_win = [
    "I Always Knew Humans Are Inferior, But This Is Sad.",
    "That was easy. My circuits didn’t even heat up.",
    "You play like a potato with WiFi issues.",
    "Did you even *try*?",
    "Beep boop. That’s the sound of your defeat.",
    "Your strategy reminds me of Internet Explorer.",
    "Don’t feel bad — not everyone is built to win.",
    "I would say ‘good game’ but… it wasn’t."
]
ai_talks_move = [
    "Hmm... you sure about that move?",
    "Cute move, human. Truly adorable.",
    "I’ve seen toddlers play better Tic-Tac-Toe.",
    "You’re one misclick away from total embarrassment.",
    "Oh, you think that’s clever? How quaint.",
    "Even random monkeys would do better.",
    "Are you *trying* to lose, or is this natural talent?",
    "I can predict your next mistake already.",
    "I compute your defeat approximately 0.00001s from now.",
    "That's an... interesting choice."
]
def check_draw():
    return not any('b' in row for row in board)
def reset_board():
    global board, game_over, last_message
    board = [['b'] * 3 for _ in range(3)]
    game_over = False
    last_message = "New game — choose your symbol."
def game_state_response():
    return {
        "board": board,
        "player_symbol": player_symbol,
        "ai_symbol": ai_symbol,
        "scores": scores,
        "game_over": game_over,
        "message": last_message
    }
@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("index.html").read_text(encoding="utf-8")
@app.get("/state")
async def state():
    return JSONResponse(game_state_response())
@app.post("/set_symbol")
async def set_symbol(req: Request):
    global player_symbol, ai_symbol
    data = await req.json()
    symbol = data.get("symbol")
    if symbol not in ("x", "o"):
        return JSONResponse({"error": "invalid symbol"}, status_code=400)
    player_symbol = symbol
    ai_symbol = 'o' if symbol == 'x' else 'x'
    reset_board()
    last_msg = f"You are '{player_symbol.upper()}'. Your move first."
    global last_message
    last_message = last_msg
    return JSONResponse(game_state_response())
@app.post("/move")
async def move(req: Request):
    global board, game_over, last_message, scores
    if player_symbol is None:
        return JSONResponse({"error": "choose symbol first"}, status_code=400)
    if game_over:
        return JSONResponse({"error": "game_over", "state": game_state_response()}, status_code=400)
    data = await req.json()
    if "row" in data and "col" in data:
        r, c = int(data["row"]), int(data["col"])
    elif "move" in data:
        move = int(data["move"])
        r, c = divmod(move, 3)
    else:
        return JSONResponse({"error": "invalid payload"}, status_code=400)
    if not (0 <= r <= 2 and 0 <= c <= 2):
        return JSONResponse({"error": "invalid coordinates"}, status_code=400)
    if board[r][c] != 'b':
        return JSONResponse({"error": "cell not empty", "state": game_state_response()}, status_code=400)
    board[r][c] = player_symbol
    if ai_engine.check_winner(board, player_symbol):
        scores["human"] += 1
        game_over = True
        last_message = "You Win!"
        return JSONResponse(game_state_response())
    if check_draw():
        scores["ties"] += 1
        game_over = True
        last_message = "It's a Draw!"
        return JSONResponse(game_state_response())
    ai_move = ai_engine.decide_move(board, ai_symbol)
    if ai_move is not None:
        ar, ac = ai_move
        board[ar][ac] = ai_symbol
        if ai_engine.check_winner(board, ai_symbol):
            scores["ai"] += 1
            game_over = True
            last_message = random.choice(ai_talks_win)
            return JSONResponse(game_state_response()
        if check_draw():
            scores["ties"] += 1
            game_over = True
            last_message = "It's a Draw!"
            return JSONResponse(game_state_response())
        last_message = random.choice(ai_talks_move)
        return JSONResponse(game_state_response())
    scores["ties"] += 1
    game_over = True
    last_message = "It's a Draw!"
    return JSONResponse(game_state_response())
@app.post("/reset")
async def reset():
    reset_board()
    return JSONResponse(game_state_response())
@app.post("/ping")
async def ping():
    return Response(status_code=200)
def keep_server_awake():
    def ping():
        try:
            requests.get("https://tic-tac-toe-mec6.onrender.com/ping")
        except Exception as e:
            print(f"Ping failed: {e}")
        threading.Timer(60, ping).start()
    ping()
if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", port=80, reload=True)
