class TicTacToe:
    def __init__(self):
        self.board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        self.player1 = 'X'
        self.player2 = 'O'
        self.game_over = False

    def print_board(self):
        for i in range(3):
            j = 0
            print(f'{self.board[i][j]} | {self.board[i][j+1]} | {self.board[i][j+2]}')
            if i != 2:
                print('---------')
                
    def make_move(self, i, j):
        if self.board[i][j] == ' ':
            self.board[i][j] = self.player1
            if self.check_winner():
                self.print_board()
                print('Player 1 wins!')
                self.game_over = True
            if self.check_draw():
                self.print_board()
                print('Draw!')
                self.game_over = True
            return True
        return False
    
    def undo_move(self, i, j):
        self.board[i][j] = ' '

    def check_winner(self) -> bool:
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != ' ':
                return True

        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != ' ':
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != ' ':
            return True

        return False

    def check_draw(self) -> bool:
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return False
        return True
    
    # Minimax algorithm - WORKS PERFECTLY, DON'T TOUCH EXCEPT TO REFACTOR
    def minimax(self, depth, is_maximizing):
        if self.check_winner():
            return 1 if not is_maximizing else -1
        if self.check_draw():
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.player2
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.player1
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score
    
    def play_against_player(self):
        while not self.game_over:
            self.print_board()
            
            # Player 1
            print('Player 1')
            while True:
                row = int(input('Enter row (1-3): '))
                col = int(input('Enter col (1-3): '))
                if 1 <= row <= 3 and 1 <= col <= 3 and self.board[row - 1][col - 1] == ' ':
                    self.board[row - 1][col - 1] = self.player1
                    break
                else:
                    print('Invalid move. Try again.')
            
            if self.check_winner():
                self.print_board()
                print('Player 1 wins!')
                self.game_over = True
                break
            if self.check_draw():
                self.print_board()
                print('Draw!')
                self.game_over = True
                break

            self.print_board()
            
            # Player 2
            print('Player 2')
            while True:
                row = int(input('Enter row (1-3): '))
                col = int(input('Enter col (1-3): '))
                if 1 <= row <= 3 and 1 <= col <= 3 and self.board[row - 1][col - 1] == ' ':
                    self.board[row - 1][col - 1] = self.player2
                    break
                else:
                    print('Invalid move. Try again.')
            
            if self.check_winner():
                self.print_board()
                print('Player 2 wins!')
                self.game_over = True
                break
            if self.check_draw():
                self.print_board()
                print('Draw!')
                self.game_over = True
                break
    
    def play_against_ai(self, player1_turn=True):
        while not self.game_over:
            self.print_board()
            
            if player1_turn:
                # Player 1
                print('Player 1')
                while True:
                    row = int(input('Enter row (1-3): '))
                    col = int(input('Enter col (1-3): '))
                    if 1 <= row <= 3 and 1 <= col <= 3 and self.board[row - 1][col - 1] == ' ':
                        self.board[row - 1][col - 1] = self.player1
                        break
                    else:
                        print('Invalid move. Try again.')
            else:
                # AI
                best_score = -float('inf')
                best_move = None
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == ' ':
                            self.board[i][j] = self.player2
                            score = self.minimax(0, False)
                            self.board[i][j] = ' '
                            if score > best_score:
                                best_score = score
                                best_move = (i, j)
                self.board[best_move[0]][best_move[1]] = self.player2
                print(f'AI placed at ({best_move[0] + 1}, {best_move[1] + 1})')
            
            if self.check_winner():
                self.print_board()
                if player1_turn:
                    print('Player 1 wins!')
                else:
                    print('AI wins!')
                self.game_over = True
                break
            if self.check_draw():
                self.print_board()
                print('Draw!')
                self.game_over = True
                break
            
            player1_turn = not player1_turn

def main():
    game = TicTacToe()
    
    print('Welcome to Tic Tac Toe!')
    print('Player 1 is X')
    print('Player 2 is O')
    print('Would you like to play against a friend or the computer?')
    print('1. Friend')
    print('2. Computer')
    choice = int(input('Enter choice (1 or 2): '))
    
    if choice == 1:
        game.play_against_player()
    elif choice == 2:
        if input('Would you like to go first? (y/n): ') == 'y'.lower():
            game.play_against_ai(True)
        else:
            game.play_against_ai(False)

if __name__ == '__main__':
    main()