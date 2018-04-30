import random

def mastermind(guess, answer):
    return ''.join(['*' for i,x in enumerate(guess) if x == answer[i]])


def main():
    print('Let\'s play a game!')
    answer = ''.join([str(random.randint(1,9)) for i in range(4)])
    guess = input('Input 4 numbers between 1 and 10 unseperated by any spaces e.g. 1234\n')
    game_over = False
    player = None
    while game_over != True:
        try:
            int(guess)
        except:
            input('Invalid input. Please try again. Input 4 numbers between 1 and 10 unseperated by any spaces e.g. 1234\n')
        else:
            player = mastermind(guess, answer)
            if player == '****':
                print('Congratulations your guess of: {guess} was correct. You win!')
                game_over = True
            else:
                print('You got the following number of values correct: {player}')
                input('Try again.\n')






