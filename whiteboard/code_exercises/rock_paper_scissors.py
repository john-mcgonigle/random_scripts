import random 

PLAYER_OPTIONS = ['rock', 'paper', 'scissors']

def main():
    play = False
    while play is False:
        print('Welcome player. Are you ready to play rock-paper-scissors?')
        answer = input().lower()
        if answer and answer[0] == 'y' or answer in ['ok','alright', 'sure']:
            play = True
    print('OK. Let\'s play rock-paper-scissors')

    turn_counter = 0
    score = 0
    while turn_counter < 3:
        score += game_turn()
        turn_counter += 1

    if score == 4.5:
        print('Game over. It\'s a tie!')
    elif score >=6:
        print('Game over. You won!')
    else:
        print('Game over. You lost!')



def game_turn(guess = None):
    guess = input('Player please enter your choice: rock, paper, or scissors.\n').lower()
    while guess not in PLAYER_OPTIONS:
        guess = input('I did not recognise that choice.\nPlease enter one of the following: rock, paper, or scissors.\n').lower()
        print('Be careful about spelling.')
    return resolve_turn(guess, random.choice(PLAYER_OPTIONS))

def resolve_turn(a, b):
    if a == b:
        print('The game is a tie, both players chose {a}.'.format(a=a))
        return 1.5
    elif a in PLAYER_OPTIONS[:2] and b in PLAYER_OPTIONS[:2]:
        if a == 'rock':
            return return_message(False, a, b)
        else:
            return return_message(True, a, b)
    elif a in PLAYER_OPTIONS[1:] and b in PLAYER_OPTIONS[1:]:
        if a == 'paper':
            return return_message(False, a, b)
        else:
            return return_message(True, a, b)
    else:
        if a == 'scissors':
            return return_message(False, a, b)
        else:
            return return_message(True, a, b)

def return_message(win, a, b):
    if win:
        print('Player wins.\nPlayer chose {a} and the computer chose {b} and {a} trumps {b}'.format(b=b, a=a))
        return 3
    else:
        print('Player loses to the computer.\nPlayer chose {a} and the computer chose {b} and {b} trumps {a}'.format(b=b, a=a))
        return 0


if __name__ == '__main__':
    main()