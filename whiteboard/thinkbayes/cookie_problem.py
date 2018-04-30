# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

bowl1 = ['Vanilla']*30 + ['Chocolate']*10
bowl2 = ['Vanilla']*20 + ['Chocolate']*20

# Trying to decide that if we drew a vanilla cookie, what is the probability of 
## being from bowl 1.


def bayes_theorm(A, B_given_A, B):
    '''
    Returns the probablity of A_given_B according to Bayes theorm when provided
    with:
        The probability of A
        The probablity of B_given_A
        The probability of B
    
    Formula:
        P(A|B) = (P(A)*P(B|A))/P(B)
    '''
    
    return (A*B_given_A)/B


# So for our problem defined above:
A = 1/2 # The chance that we selected bowl1 out of the 2 bowls. 
B= (bowl1.count('Vanilla')+bowl2.count('Vanilla'))/ (len(bowl1) + len(bowl2))
B_given_A = bowl1.count('Vanilla')/len(bowl1)


bayes_theorm(A, B_given_A, B)
