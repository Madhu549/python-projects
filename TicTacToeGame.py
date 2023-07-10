# Tic Tac Toe project
# Board printing
from IPython.display import clear_output
def board_printing(board_list):
    clear_output()
    print(board_list[0] ,Fore.LIGHTWHITE_EX +'|' ,board_list[1],'|' ,board_list[2])
    print(Fore.LIGHTWHITE_EX + '---------')
    print(board_list[3] ,'|' ,board_list[4] ,'|' ,board_list[5])
    print(Fore.LIGHTWHITE_EX + '---------')
    print(board_list[6],'|' ,board_list[7] , '|' ,board_list[8])


# print(board_printing(board_list))


# Taking players input
def player_input():
    player = ''
    while player != 'X' and player != 'O':
        player = input('Player1 enter X or O: ').upper()
    if player == 'X':
        return ('X', 'O')
    else:
        return ('O', 'X')


# print(player_input())

# place marker at a index
def place_marker(board_list, player, index):
    board_list[index] = player


# print(place_marker(board_list,'x',3))

# Check the winner
def win_check(board_list, player):
    return (board_list[0] == board_list[1] == board_list[2] == player) or (
                board_list[3] == board_list[4] == board_list[5] == player) or (
                       board_list[6] == board_list[7] == board_list[8] == player) or (
                       board_list[0] == board_list[3] == board_list[6] == player) or (
                       board_list[1] == board_list[4] == board_list[7] == player) or (
                       board_list[2] == board_list[5] == board_list[8] == player) or (
                       board_list[0] == board_list[4] == board_list[8] == player) or (
                       board_list[2] == board_list[4] == board_list[6] == player)


# print(win_check(board_list,'X'))

# who is first
import random


def choose_first():
    flip = random.randint(0, 1)
    if flip == 0:
        return 'Player 1'
    else:
        return 'Player 2'


# print(choose_first())

# space available or not in the board
def space_check(board_list, position):
    return board_list[position] == ' '


# print(space_check(board_list,3))

# check for board is full condition
def check_board_full(board_list):
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        if space_check(board_list, i):
            return False
    return True


# print(check_board_full(board_list))
# check for players choice of index
def player_choice(board_list):
    position = -1
    while position not in range(0, 9) or not space_check(board_list, position):
        position = int(input('enter a position in between(0-8): '))
    return position


# print(player_choice(board_list))

# replay the game?
def replay():
    choice = input("Do you want to play the game again ? (Y|N): ").upper()
    return choice == 'Y'


# replay()

# main logic Of Tic Tac Toe Game
from colorama import init,Fore
init()
print(Fore.RED+"====Welcome to Tic Tac Toe====")

while True:

    # setting things ready
    board = [' '] * 10
    player1_marker, player2_marker = player_input()
    player_turn = choose_first()
    print(player_turn + Fore.BLUE + " Will go First!!!!!.")
    play_game = input(Fore.MAGENTA+"Ready to play the Game? (Y|N): ").upper()
    if play_game == 'Y':
        game_on = True
    else:
        game_on = False
    while game_on:
        # player 1 Turn
        if player_turn == 'Player 1':
            board_printing(board)
            position = player_choice(board)
            place_marker(board, player1_marker, position)

            if win_check(board, player1_marker):
                board_printing(board)
                print(Fore.CYAN + 'Player 1 has won the match !!!:).')
                game_on = False
            else:
                if check_board_full(board):
                    board_printing(board)
                    print(Fore.BLACK + "It's a Tie!!!!")
                    game_on = False
                else:
                    player_turn = 'Player 2'
        # player 2 Turn
        else:
            board_printing(board)
            position = player_choice(board)
            place_marker(board, player2_marker, position)

            if win_check(board, player2_marker):
                board_printing(board)
                print(Fore.CYAN + 'Player 2 has won the match !!!:).')
                game_on = False
            else:
                if check_board_full(board):
                    board_printing(board)
                    print(Fore.BLACK + "It's a Tie!!!!")
                    game_on = False
                else:
                    player_turn = 'Player 1'

    if not replay():
        break