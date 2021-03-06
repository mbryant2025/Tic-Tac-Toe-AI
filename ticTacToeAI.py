import random

class board:

    def __init__(self, moves = list(range(9))):
        self.spaces = moves
        
    def printBoard(self):
        print()
        string = ""
        string = string.join([str(space) for space in self.spaces])
        for i in range(3):
            print(string[3 * i] + " | " + string[3 * i + 1] + " | " + string[3 * i + 2])
            if i != 2:
                print("---------")
        print()

    def try_move(self, symbol, space):
        if space is None:
            return False
        if type(self.spaces[space]) is int:
            self.spaces[space] = symbol
            return True
        else:
            return False

    def prompt_move(self):
        move = None
        first_round = True
        while 1:
            if move is not None and 0 <= move <= 8 and self.try_move("X", move):
                break
            else:
                if not first_round:
                    print("Invalid input")
                try:
                    move = int(input("Player X: Enter a space:\t"))
                except:
                    pass
                first_round = False

    def get_game_state(self):
        state = "ongoing"
        winner = None

        #check for column win
        for c in range(3):
            if self.spaces[c] == self.spaces[c + 3] == self.spaces[c + 6]:
                state = "over"
                winner = self.spaces[c]

        #check for row win
        for r in range(0, 9, 3):
            if self.spaces[r] == self.spaces[r + 1] == self.spaces[r + 2]:
                state = "over"
                winner = self.spaces[r]

        #check diagonals for win
        if self.spaces[2] == self.spaces[4] == self.spaces[6]:
            state = "over"
            winner = self.spaces[2]

        if self.spaces[0] == self.spaces[4] == self.spaces[8]:
            state = "over"
            winner = self.spaces[0]

        #check for tie
        if state != "over" and len([x for x in self.spaces if type(x) is int]) == 0:
            state = "tie"

        return state, winner

    def has_winning_move(self, symbol):

        potential_winner = False
        winning_moves = []

        #check for column winning move
        for c in range(3):
            column = [self.spaces[c], self.spaces[c + 3], self.spaces[c + 6]]
            if column.count(symbol) == 2 and len([x for x in column if type(x) is int]) == 1:
                potential_winner = True
                winning_moves.extend(x for x in column if type(x) is int)

        #check for row winning move
        for r in range(0, 9, 3):
            row = [self.spaces[r], self.spaces[r + 1], self.spaces[r + 2]]
            if row.count(symbol) == 2 and len([x for x in row if type(x) is int]) == 1:
                potential_winner = True
                winning_moves.extend(x for x in row if type(x) is int)

        #check for diagonal winning move
        diags = [[self.spaces[0], self.spaces[4], self.spaces[8]], [self.spaces[2], self.spaces[4], self.spaces[6]]]
        for diag in diags:
            if diag.count(symbol) == 2 and len([x for x in diag if type(x) is int]) == 1:
                    potential_winner = True
                    winning_moves.extend(x for x in diag if type(x) is int)

        return potential_winner, winning_moves

    def fork_moves(self, symbol):

        fork_moves = []

        for i in range(9):
            temp_board = board(list(self.spaces))
            temp_board.try_move(symbol, i)
            if len(temp_board.has_winning_move(symbol)[1]) > 1:
                fork_moves.append(i)
            del temp_board

        return fork_moves

    def can_play_opposite_corner(self, opponent_symbol):

        options = []
        corners = [[self.spaces[0], self.spaces[8]], [self.spaces[2], self.spaces[6]]]

        for i in range(2):
            if opponent_symbol in corners[i] and len([x for x in corners[i] if type(x) is int]) == 1:
                if(corners[i].index(opponent_symbol) == 0):
                    options.append(8)
                if(corners[i].index(opponent_symbol) == 8):
                    options.append(0)
                if(corners[i].index(opponent_symbol) == 2):
                    options.append(6)
                if(corners[i].index(opponent_symbol) == 6):
                    options.append(2)

        return len(options) > 0, options


def run_game():

    gameboard = board(list(range(9)))
    turn = "human"
    state = "ongoing"
    while state == "ongoing":
        if turn == "human":
            gameboard.printBoard()
            gameboard.prompt_move()
            turn = "computer"
        elif turn == "computer":
            if gameboard.has_winning_move("O")[0]:
                gameboard.try_move("O", random.choice(gameboard.has_winning_move("O")[1]))
            elif gameboard.has_winning_move("X")[0]:
                gameboard.try_move("O", random.choice(gameboard.has_winning_move("X")[1]))
            elif len(gameboard.fork_moves("O")) > 0:
                gameboard.try_move("O", random.choice(gameboard.fork_moves("O")))
            elif len(gameboard.fork_moves("X")) > 0:
                if len(gameboard.fork_moves("X")) > 1:
                    if gameboard.spaces[0] == "X" and gameboard.spaces[8] == "X" and gameboard.spaces[4] == "O" or gameboard.spaces[2] == "X" and gameboard.spaces[6] == "X" and gameboard.spaces[4] == "O":
                        gameboard.try_move("O", random.choice([1, 3, 5, 7]))
                    elif gameboard.spaces[4] == "X" and (gameboard.spaces[0] == "X" or gameboard.spaces[2] == "X" or gameboard.spaces[6] == "X" or gameboard.spaces[8] == "X"):
                        if gameboard.spaces[2] == "X" or gameboard.spaces[6] == "X":
                            gameboard.try_move("O", random.choice([0, 8]))
                        else:
                            gameboard.try_move("O", random.choice([2, 6]))
                    elif gameboard.spaces[4] == "O" and (gameboard.spaces[0] == gameboard.spaces[6] == "X" or gameboard.spaces[0] == gameboard.spaces[2] == "X" or gameboard.spaces[2] == gameboard.spaces[8] == "X" or gameboard.spaces[6] == gameboard.spaces[8] == "X"):
                        while not (gameboard.try_move("O", random.choice([1, 3, 5, 7]))):
                            pass
                else:
                    gameboard.try_move("O", random.choice(gameboard.fork_moves("X")))
            elif gameboard.spaces[4] == 4:
                gameboard.try_move("O", 4)
            elif gameboard.can_play_opposite_corner("X")[0]:
                gameboard.try_move("O", random.choice(gameboard.can_play_opposite_corner("X")[1]))
            elif len([x for x in gameboard.spaces if x == 0 or x == 2 or x == 6 or x == 8]) > 0:
                while not (gameboard.try_move("O", random.choice([0, 2, 6, 8]))):
                    pass
            else:
                while not (gameboard.try_move("O", random.choice([1, 3, 5, 7]))):
                    pass
            turn = "human"
        state, winner = gameboard.get_game_state()
    gameboard.printBoard()
    if state == "tie":
        print("The game was a tie")
    elif state == "over":
        print(winner + " wins!")
    del gameboard
        
run_game()
while 1:
    print()
    if input("Play again? Press [enter] to continue, enter any key to exit.\t") == "":
        run_game()
    else:
        break
