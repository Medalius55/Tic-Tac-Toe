import tkinter as tk
from tictactoe import TicTacToe as ttt

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x700")
        self.game = ttt()
        self.ai = False  # Flag to indicate if playing against AI
        
        # Create main frames
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        
        self.board_frame = tk.Frame(self.root)
        self.text_frame = tk.Frame(self.root)
        
        # Create starting screen
        self.create_start_screen()
        
        # Create game widgets
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        
        # Create label for on-screen text
        self.label = tk.Label(self.text_frame, text="Player X's turn", font=('Georgia', 20))
        self.label.pack()

        # Create "Play Again?" button (initially hidden)
        self.play_again_button = tk.Button(self.text_frame, text="Play Again?", font=('Georgia', 20), command=self.reset_board)
        self.play_again_button.pack(pady=20)
        self.play_again_button.pack_forget()

        # Create "Return to Main Menu" button (initially hidden)
        self.return_button = tk.Button(self.text_frame, text="Return to Main Menu", font=('Georgia', 20), command=self.return_to_main_menu)
        self.return_button.pack(pady=20)
        self.return_button.pack_forget()

    def create_start_screen(self):
        # Clear the start frame before adding new widgets
        for widget in self.start_frame.winfo_children():
            widget.destroy()
        
        start_label = tk.Label(self.start_frame, text="Welcome to Tic Tac Toe!", font=('Georgia', 30))
        start_label.pack(pady=50)
        
        play_ai_button = tk.Button(self.start_frame, text="Play Against AI", font=('Georgia', 20), command=self.choose_ai_options)
        play_ai_button.pack(pady=20)
        
        play_human_button = tk.Button(self.start_frame, text="Play Against Player", font=('Georgia', 20), command=lambda: self.start_game(ai=False))
        play_human_button.pack(pady=20)
        
    def choose_ai_options(self):
        # Clear the start frame before adding new widgets
        for widget in self.start_frame.winfo_children():
            widget.destroy()
        
        choose_label = tk.Label(self.start_frame, text="Choose who goes first:", font=('Georgia', 20))
        choose_label.pack(pady=20)
        
        player_first_button = tk.Button(self.start_frame, text="Player First", font=('Georgia', 20), command=lambda: self.start_game(ai=True, player1_turn=True))
        player_first_button.pack(pady=10)
        
        ai_first_button = tk.Button(self.start_frame, text="AI First", font=('Georgia', 20), command=lambda: self.start_game(ai=True, player1_turn=False))
        ai_first_button.pack(pady=10)

    def start_game(self, ai=False, player1_turn=True):
        self.start_frame.pack_forget()
        self.board_frame.pack(side=tk.TOP, pady=20)
        self.text_frame.pack(side=tk.BOTTOM, pady=20)
        self.label.pack()
        
        self.ai = ai
        self.player1_turn = player1_turn
        
        if not player1_turn and ai:
            self.ai_move()

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text=' ', font=('Georgia', 40), width=5, height=2, 
                                   command=lambda i=i, j=j: self.on_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def on_click(self, i, j):
        if self.game.board[i][j] == ' ':
            self.game.board[i][j] = self.game.player1 if self.player1_turn else self.game.player2
            self.update_buttons()
            self.root.update()  # Force the GUI to update before showing the message box
            if self.game.check_winner():
                self.label.config(text=f"Player {'X' if self.player1_turn else 'O'} wins!")
                self.disable_buttons()
                self.play_again_button.pack()  # Show the "Play Again?" button
                self.return_button.pack()  # Show the "Return to Main Menu" button
            elif self.game.check_draw():
                self.label.config(text="It's a draw!")
                self.disable_buttons()
                self.play_again_button.pack()  # Show the "Play Again?" button
                self.return_button.pack()  # Show the "Return to Main Menu" button
            else:
                self.player1_turn = not self.player1_turn
                self.label.config(text=f"Player {'X' if self.player1_turn else 'O'}'s turn")
                if self.ai and not self.player1_turn:
                    self.ai_move()

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] == ' ':
                    self.game.board[i][j] = self.game.player2
                    score = self.game.minimax(0, False)
                    self.game.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        self.game.board[best_move[0]][best_move[1]] = self.game.player2
        self.update_buttons()
        self.root.update()  # Force the GUI to update before showing the message box
        if self.game.check_winner():
            self.label.config(text="AI wins!")
            self.disable_buttons()
            self.play_again_button.pack()  # Show the "Play Again?" button
            self.return_button.pack()  # Show the "Return to Main Menu" button
        elif self.game.check_draw():
            self.label.config(text="It's a draw!")
            self.disable_buttons()
            self.play_again_button.pack()  # Show the "Play Again?" button
            self.return_button.pack()  # Show the "Return to Main Menu" button
        else:
            self.player1_turn = not self.player1_turn
            self.label.config(text=f"Player {'X' if self.player1_turn else 'O'}'s turn")

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.game.board[i][j])

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)

    def reset_board(self):
        self.game = ttt()
        self.update_buttons()
        self.label.config(text="Player X's turn")
        if self.ai and not self.player1_turn:
            self.ai_move()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.NORMAL)
        self.play_again_button.pack_forget()  # Hide the "Play Again?" button
        self.return_button.pack_forget()  # Hide the "Return to Main Menu" button

    def return_to_main_menu(self):
        self.reset_board()
        self.board_frame.pack_forget()
        self.text_frame.pack_forget()
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        self.create_start_screen()  # Ensure the start screen is recreated

def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()