import customtkinter as ctk
import tkinter as tk
import math
import random
import time

# ==========================================
# 🧠 CORE AI ENGINE (Alpha-Beta & Minimax)
# ==========================================
class AIEngine:
    def __init__(self):
        self.win_states = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        self.match_nodes = 0 
        self.match_time = 0.0 

    def check_winner(self, board):
        for state in self.win_states:
            if board[state[0]] == board[state[1]] == board[state[2]] and board[state[0]] != "":
                return board[state[0]], state
        if "" not in board:
            return "Tie", None
        return None, None

    def utility(self, board, maximizing_player, depth):
        winner, _ = self.check_winner(board)
        if not winner: return None
        if winner == "Tie": return 0
        return 10 - depth if winner == maximizing_player else -10 + depth

    def minimax(self, board, depth, is_maximizing, maximizing_player):
        self.match_nodes += 1 
        winner, _ = self.check_winner(board)
        if winner: return self.utility(board, maximizing_player, depth)

        current_mark = maximizing_player if is_maximizing else ("X" if maximizing_player == "O" else "O")
        best_score = -math.inf if is_maximizing else math.inf

        for i in range(9):
            if board[i] == "":
                board[i] = current_mark
                score = self.minimax(board, depth + 1, not is_maximizing, maximizing_player)
                board[i] = ""
                best_score = max(score, best_score) if is_maximizing else min(score, best_score)
        return best_score

    def alphabeta(self, board, depth, alpha, beta, is_maximizing, maximizing_player):
        self.match_nodes += 1 
        winner, _ = self.check_winner(board)
        if winner: return self.utility(board, maximizing_player, depth)

        current_mark = maximizing_player if is_maximizing else ("X" if maximizing_player == "O" else "O")
        best_score = -math.inf if is_maximizing else math.inf

        for i in range(9):
            if board[i] == "":
                board[i] = current_mark
                score = self.alphabeta(board, depth + 1, alpha, beta, not is_maximizing, maximizing_player)
                board[i] = ""
                
                if is_maximizing:
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                else:
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                
                if beta <= alpha: break 
        return best_score

    def get_move(self, board, ai_player, algo_mode, difficulty):
        start_time = time.perf_counter() 
        
        empty_cells = [i for i in range(9) if board[i] == ""]
        if not empty_cells: return None
        
        rand_chance = {"EASY": 0.75, "NORMAL": 0.40, "HARD": 0.10, "VERY HARD": 0.0}.get(difficulty, 0.0)

        if random.random() < rand_chance:
            move = random.choice(empty_cells)
            self.match_time += (time.perf_counter() - start_time)
            return move

        best_score = -math.inf
        best_move = empty_cells[0]

        for i in empty_cells:
            board[i] = ai_player
            if algo_mode == "ALPHA-BETA":
                score = self.alphabeta(board, 0, -math.inf, math.inf, False, ai_player)
            else:
                score = self.minimax(board, 0, False, ai_player)
            board[i] = ""
            
            if score > best_score:
                best_score = score
                best_move = i

        self.match_time += (time.perf_counter() - start_time)
        return best_move


# ==========================================
# 📐 CUSTOM SCI-FI CHAMFERED BUTTON WIDGET
# ==========================================
class SciFiButton(tk.Canvas):
    def __init__(self, master, text, subtext="", color="#FF0000", command=None, width=320, height=75, bg_color="#0A0B1A"):
        super().__init__(master, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.command = command
        self.color = color
        self.bg_color = bg_color
        self.hover_color = "#12142B" # Universal Sci-Fi Hover Tone
        
        c = 18 
        w, h = width, height
        self.pts = [c, 3, w-3, 3, w-3, h-c, w-c, h-3, 3, h-3, 3, c]
        
        self.poly_glow = self.create_polygon(self.pts, outline=color, fill="", width=6, stipple="gray50")
        self.poly_main = self.create_polygon(self.pts, outline="#FFFFFF", fill=self.bg_color, width=2)
        
        text_y = h//2 if not subtext else h//2 - 10
        self.create_text(w//2, text_y, text=text, fill="#FFFFFF", font=("Impact", 22), tags="btn")
        if subtext:
            self.create_text(w//2, h//2 + 15, text=subtext, fill="#DDDDDD", font=("Arial", 11, "bold"), tags="btn")
            
        self.addtag_all("btn")
        self.tag_bind("btn", "<Enter>", self.on_enter)
        self.tag_bind("btn", "<Leave>", self.on_leave)
        self.tag_bind("btn", "<Button-1>", self.on_click)
        self.tag_bind("btn", "<ButtonRelease-1>", self.on_release)
        
    def on_enter(self, e):
        self.itemconfig(self.poly_main, fill=self.hover_color)
    def on_leave(self, e):
        self.itemconfig(self.poly_main, fill=self.bg_color)
    def on_click(self, e):
        self.itemconfig(self.poly_main, fill=self.color)
    def on_release(self, e):
        self.itemconfig(self.poly_main, fill=self.hover_color)
        if self.command:
            self.command()


# ==========================================
# 🎮 MAIN APPLICATION (Dual-Tone Theme)
# ==========================================
class UltimateSciFiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Neon AI Championship - Dual Tone")
        self.geometry("900x750")
        self.minsize(800, 700) 
        
        # Deep Sci-Fi Void Background
        self.bg_color = "#06050B" 
        self.configure(fg_color=self.bg_color) 
        
        self.engine = AIEngine()
        self.board = [""] * 9
        self.game_active = False
        self.current_turn = "X"
        self.mode = ""         
        self.algo_mode = ""    
        self.difficulty = ""   
        
        self.p_wins = 0
        self.p_losses = 0
        self.p_ties = 0
        
        # 🎨 THE NEW DUAL-TONE PALETTE
        self.pal = {
            "red": "#FF0044",      # Crimson for O & Aggressive Elements
            "cyan": "#00D0FF",     # Electric Blue for X & Tech Elements
            "green": "#00FF66",    # Success / Restart
            "gold": "#FFD700",     # Premium / Hard Mode / Nodes
            "white": "#FFFFFF", 
            "panel": "#0D0A14",    # Dark glass panel color
            "border": "#21162B"    # Panel borders
        }

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both")
        
        self.setup_ui_screens()
        self.show_frame(self.menu_frame)


    def show_frame(self, target):
        for f in (self.menu_frame, self.algo_frame, self.diff_frame, self.game_frame, self.res_frame):
            f.pack_forget()
        target.pack(fill="both", expand=True)

    def setup_ui_screens(self):
        # --- 1. MAIN MENU ---
        self.menu_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.menu_center = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.menu_center.pack(expand=True)
        
        ctk.CTkLabel(self.menu_center, text="TIC-TAC-TOE", font=("Impact", 85), text_color="#FFF").pack(pady=(0, 0))
        ctk.CTkLabel(self.menu_center, text="CHAMPIONSHIP", font=("Impact", 55), text_color=self.pal["cyan"]).pack(pady=(0, 50))

        # Dual tone buttons
        SciFiButton(self.menu_center, "VS CPU", "", self.pal["cyan"], lambda: self.route_mode("PvE"), bg_color=self.bg_color).pack(pady=10)
        SciFiButton(self.menu_center, "2PLAYER", "", self.pal["red"], lambda: self.route_mode("PvP"), bg_color=self.bg_color).pack(pady=10)

        # --- 2. ALGO MENU ---
        self.algo_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.algo_center = ctk.CTkFrame(self.algo_frame, fg_color="transparent")
        self.algo_center.pack(expand=True)
        
        ctk.CTkLabel(self.algo_center, text="CORE ALGORITHM", font=("Impact", 55), text_color="#FFF").pack(pady=(0, 40))
        
        SciFiButton(self.algo_center, "MINIMAX", "Exhaustive Search", self.pal["cyan"], lambda: self.route_algo("MINIMAX"), bg_color=self.bg_color).pack(pady=10)
        SciFiButton(self.algo_center, "ALPHA-BETA", "Pruned Optimization", self.pal["red"], lambda: self.route_algo("ALPHA-BETA"), bg_color=self.bg_color).pack(pady=10)
        
        ctk.CTkButton(self.algo_center, text="← BACK TO MAIN MENU", font=("Arial", 14, "bold"), fg_color="transparent", 
                      text_color="#888", hover_color="#181124", command=lambda: self.show_frame(self.menu_frame)).pack(pady=40)

        # --- 3. DIFFICULTY MENU ---
        self.diff_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.diff_center = ctk.CTkFrame(self.diff_frame, fg_color="transparent")
        self.diff_center.pack(expand=True)
        
        ctk.CTkLabel(self.diff_center, text="DIFFICULTY", font=("Impact", 55), text_color=self.pal["gold"]).pack(pady=(0, 30))
        
        # Multicolored progression
        SciFiButton(self.diff_center, "EASY", "Winning Rate : 100 %", self.pal["cyan"], lambda: self.start_match("EASY"), bg_color=self.bg_color).pack(pady=8)
        SciFiButton(self.diff_center, "NORMAL", "Winning Rate : 75 %", self.pal["green"], lambda: self.start_match("NORMAL"), bg_color=self.bg_color).pack(pady=8)
        SciFiButton(self.diff_center, "HARD", "Winning Rate : 22 %", self.pal["gold"], lambda: self.start_match("HARD"), bg_color=self.bg_color).pack(pady=8)
        SciFiButton(self.diff_center, "VERY HARD", "Winning Rate : 0 %", self.pal["red"], lambda: self.start_match("VERY HARD"), bg_color=self.bg_color).pack(pady=8)
        
        ctk.CTkButton(self.diff_center, text="← RETURN TO ALGORITHMS", font=("Arial", 14, "bold"), fg_color="transparent", 
                      text_color="#888", hover_color="#181124", command=lambda: self.show_frame(self.algo_frame)).pack(pady=20)

        # --- 4. GAME ARENA ---
        self.game_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.game_center = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.game_center.pack(expand=True)
        
        self.status_header = ctk.CTkLabel(self.game_center, text="MATCH STARTED", font=("Impact", 40), text_color="#FFF")
        self.status_header.pack(pady=(0, 20))

        self.grid_wrapper = ctk.CTkFrame(self.game_center, fg_color="transparent")
        self.grid_wrapper.pack(pady=10)
        
        self.grid_slots = []
        for i in range(9):
            btn = ctk.CTkButton(
                self.grid_wrapper, text="", font=("Impact", 75),
                fg_color="transparent", border_color=self.pal["border"], border_width=4,
                hover_color=self.pal["panel"], corner_radius=16, width=135, height=135,
                command=lambda idx=i: self.process_click(idx)
            )
            btn.grid(row=i//3, column=i%3, padx=8, pady=8)
            self.grid_slots.append(btn)

        self.game_action_bar = ctk.CTkFrame(self.game_center, fg_color="transparent")
        self.game_action_bar.pack(pady=30)
        
        f1 = ctk.CTkFrame(self.game_action_bar, fg_color="transparent")
        f1.pack(side="left", padx=10)
        SciFiButton(f1, "↻ RESTART", "", self.pal["green"], self.action_restart, width=220, height=55, bg_color=self.bg_color).pack()
        
        f2 = ctk.CTkFrame(self.game_action_bar, fg_color="transparent")
        f2.pack(side="left", padx=10)
        SciFiButton(f2, "≡ MENU", "", self.pal["cyan"], self.action_quit, width=220, height=55, bg_color=self.bg_color).pack()

        # --- 5. RESULT SCREEN ---
        self.res_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.res_center = ctk.CTkFrame(self.res_frame, fg_color="transparent")
        self.res_center.pack(expand=True)
        
        self.res_diff_label = ctk.CTkLabel(self.res_center, text="EASY", font=("Arial", 16, "bold"), text_color="#FFF")
        self.res_diff_label.pack(pady=(0, 5))
        self.res_main_label = ctk.CTkLabel(self.res_center, text="YOU LOSE", font=("Impact", 70), text_color=self.pal["red"])
        self.res_main_label.pack(pady=(0, 15))

        self.record_panel = ctk.CTkFrame(self.res_center, fg_color=self.pal["panel"], corner_radius=15, border_width=2, border_color=self.pal["border"], width=480, height=210)
        self.record_panel.pack(pady=5)
        self.record_panel.pack_propagate(False)
        
        ctk.CTkLabel(self.record_panel, text="MATCH RECORD", font=("Arial", 14, "bold"), text_color="#888").pack(pady=(15, 10))
        
        self.split_frame = ctk.CTkFrame(self.record_panel, fg_color="transparent")
        self.split_frame.pack(fill="x", padx=40)
        self.split_frame.grid_columnconfigure(0, weight=1)
        self.split_frame.grid_columnconfigure(1, weight=0)
        self.split_frame.grid_columnconfigure(2, weight=1)

        self.win_box = ctk.CTkFrame(self.split_frame, fg_color="transparent")
        self.win_box.grid(row=0, column=0)
        ctk.CTkLabel(self.win_box, text="WIN", font=("Impact", 24), text_color=self.pal["cyan"]).pack()
        self.lbl_win_count = ctk.CTkLabel(self.win_box, text="0", font=("Impact", 45), text_color="#FFF")
        self.lbl_win_count.pack()

        ctk.CTkLabel(self.split_frame, text="|", font=("Arial", 50), text_color=self.pal["border"]).grid(row=0, column=1)

        self.lose_box = ctk.CTkFrame(self.split_frame, fg_color="transparent")
        self.lose_box.grid(row=0, column=2)
        ctk.CTkLabel(self.lose_box, text="LOSE", font=("Impact", 24), text_color=self.pal["red"]).pack()
        self.lbl_lose_count = ctk.CTkLabel(self.lose_box, text="0", font=("Impact", 45), text_color="#FFF")
        self.lbl_lose_count.pack()

        self.btn_reset_stats = ctk.CTkButton(
            self.record_panel, text="∅ CLEAR RECORD", font=("Arial", 12, "bold"), text_color="#FFF",
            fg_color="#330B1A", border_color=self.pal["red"], border_width=1, hover_color="#550B1A", 
            corner_radius=8, width=150, height=30, command=self.reset_session_stats
        )
        self.btn_reset_stats.pack(pady=(15, 0))

        # ENGINE TELEMETRY PANEL
        self.telemetry_panel = ctk.CTkFrame(self.res_center, fg_color="#0D0A14", corner_radius=10, border_width=1, border_color=self.pal["border"], width=550, height=110)
        self.telemetry_panel.pack(pady=10)
        self.telemetry_panel.pack_propagate(False)
        
        self.lbl_nodes = ctk.CTkLabel(self.telemetry_panel, text="Nodes Evaluated: 0", font=("Courier", 14, "bold"), text_color=self.pal["gold"])
        self.lbl_nodes.pack(pady=(12, 2))
        
        self.lbl_time = ctk.CTkLabel(self.telemetry_panel, text="Compute Time: 0.0000 seconds", font=("Courier", 14, "bold"), text_color=self.pal["cyan"])
        self.lbl_time.pack(pady=(0, 2))
        
        self.lbl_complexity = ctk.CTkLabel(self.telemetry_panel, text="Time Complexity: O(b^m) ≈ 362,880 Max States", font=("Courier", 14), text_color=self.pal["red"])
        self.lbl_complexity.pack()

        self.res_action_bar = ctk.CTkFrame(self.res_center, fg_color="transparent")
        self.res_action_bar.pack(pady=(15, 0))
        
        rf1 = ctk.CTkFrame(self.res_action_bar, fg_color="transparent")
        rf1.pack(side="left", padx=10)
        SciFiButton(rf1, "↻ RESTART", "", self.pal["green"], self.action_restart, width=220, height=55, bg_color=self.bg_color).pack()
        
        rf2 = ctk.CTkFrame(self.res_action_bar, fg_color="transparent")
        rf2.pack(side="left", padx=10)
        SciFiButton(rf2, "≡ MENU", "", self.pal["cyan"], self.action_quit, width=220, height=55, bg_color=self.bg_color).pack()

    # ----------------------------------------------------
    # ROUTING & LOGIC
    # ----------------------------------------------------
    def route_mode(self, choice):
        self.mode = choice
        self.show_frame(self.algo_frame)

    def route_algo(self, choice):
        self.algo_mode = choice
        if self.mode == "PvE":
            self.show_frame(self.diff_frame)
        else:
            self.difficulty = "MULTIPLAYER"
            self.action_restart()

    def start_match(self, diff):
        self.difficulty = diff
        self.action_restart()

    def action_quit(self):
        self.game_active = False
        self.show_frame(self.menu_frame)

    def action_restart(self):
        self.board = [""] * 9
        self.current_turn = "X"
        self.game_active = True
        self.engine.match_nodes = 0 
        self.engine.match_time = 0.0
        self.show_frame(self.game_frame)
        
        for slot in self.grid_slots:
            slot.configure(text="", fg_color="transparent", border_color=self.pal["border"], state="normal")
        self.update_status()

    def reset_session_stats(self):
        self.p_wins = 0
        self.p_losses = 0
        self.p_ties = 0
        self.lbl_win_count.configure(text="0")
        self.lbl_lose_count.configure(text="0")

    def update_status(self):
        msg = f"PLAYER TURN ({self.current_turn})" if self.mode == "PvP" else ("YOUR TURN (X)" if self.current_turn == "X" else "AI PROCESSING...")
        # X is Cyan, O/AI is Red
        color = self.pal["cyan"] if self.current_turn == "X" else self.pal["red"]
        self.status_header.configure(text=msg, text_color=color)
        self.update_idletasks()

    def process_click(self, index):
        if not self.game_active or self.board[index] != "": return
        if self.mode == "PvE" and self.current_turn == "O": return 
        
        self.commit_move(index)
        if self.mode == "PvE" and self.game_active:
            self.update_status()
            self.after(350, self.ai_turn)

    def commit_move(self, index):
        self.board[index] = self.current_turn
        
        # Apply Dual Tone colors to the board
        c = self.pal["cyan"] if self.current_turn == "X" else self.pal["red"]
        self.grid_slots[index].configure(text=self.current_turn, text_color=c)
        
        winner, win_line = self.engine.check_winner(self.board)
        if winner:
            self.game_active = False
            for slot in self.grid_slots: slot.configure(state="disabled")
            
            if win_line:
                for idx in win_line:
                    # Highlight winning line with its color
                    bg_color = "#0B2130" if winner == "X" else "#300B11"
                    self.grid_slots[idx].configure(fg_color=bg_color, border_color=c, text_color=c)
            
            self.after(800, lambda: self.show_results(winner)) 
        else:
            self.current_turn = "O" if self.current_turn == "X" else "X"
            self.update_status()

    def ai_turn(self):
        if not self.game_active: return
        move = self.engine.get_move(self.board, self.current_turn, self.algo_mode, self.difficulty)
        if move is not None: self.commit_move(move)

    def show_results(self, winner):
        if winner == "X":
            self.p_wins += 1
            main_txt, main_c = "YOU WIN!", self.pal["cyan"]
        elif winner == "O":
            self.p_losses += 1
            main_txt, main_c = ("TEAM O WINS!" if self.mode == "PvP" else "YOU LOSE"), self.pal["red"]
        else:
            self.p_ties += 1
            main_txt, main_c = "DRAW", self.pal["gold"]

        self.res_diff_label.configure(text=f"{self.algo_mode} // {self.difficulty}")
        self.res_main_label.configure(text=main_txt, text_color=main_c)
        self.lbl_win_count.configure(text=str(self.p_wins))
        self.lbl_lose_count.configure(text=str(self.p_losses))

        # Metric Integration
        self.lbl_nodes.configure(text=f"Total Nodes Evaluated: {self.engine.match_nodes:,}")
        
        if self.mode == "PvP":
            tc = "N/A (Human vs Human)"
            exec_time = 0.0
            self.lbl_nodes.configure(text="Total Nodes Evaluated: 0")
        else:
            exec_time = self.engine.match_time
            if self.algo_mode == "ALPHA-BETA":
                tc = "O(b^(m/2)) ≈ 19,683 Max States"
            else:
                tc = "O(b^m) ≈ 362,880 Max States"
                
        self.lbl_time.configure(text=f"Compute Time: {exec_time:.4f} seconds")
        self.lbl_complexity.configure(text=f"Time Complexity: {tc}")

        self.show_frame(self.res_frame)

if __name__ == "__main__":
    app = UltimateSciFiApp()
    app.mainloop()
