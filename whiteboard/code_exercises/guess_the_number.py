from random import randint

def main():
    print('Let\'s play a guessing game. I\'ll choose a number between 1 and 10 and you try and guess the correct number!')
    number = randint(1,10)
    game(number)

def game(number):
    game_over = False
    guess = input('OK. I\'ve chosen my number. What do you think it is?\n')
    while game_over != True:
        try:
            guess= int(guess)

        except:
            guess = input('Please enter a valid number.\n')
            continue

        print('OK. So you guessed: {guess}.'.format(guess=guess))
        if guess == number:
            print('Well done. You guessed correctly, the number was {guess}'.format(guess=guess))
            game_over = True
        else:
            decision(guess, number)
        if game_over == False:
            guess = input('Try again. Pick a number.\n')



def decision(guess, number):
    if guess < number:
        message = 'lower'
    else:
        message = 'higher'
    print('Oh no!. Your guess of {guess} was {message} than the number I chose.'.format(guess=guess, message=message))

if __name__ == '__main__':
    main()