# Liar-s-Dice-Optimal-Move
In this game of Liar's Dice each player holds two dice, ones are wild and calza is allowed.

At each decision point a player must make one of three moves; Liar, Calza or Bid.

If Player A calls Liar on Player B's Bid of x dice with face y. 
If the sum of dice with face y or one is less than x, Player B will lose a dice, otherwise, Player A will lose a dice.

If Player A calls Calza on Player B's Bid of x dice with face y. 
If the sum of dice with face y or one is less exactly x, Player A will gain a dice, otherwise, Player A will lose a dice.

This function creates a probability matrix for each combination of two dice and assigns it a probability based on bidding action.
It then evaluates the expected win probability of calling Liar or Calza. 
For evaluating the win probability of a bid, we iterate each possible bid for each possible combination of our opponent's dice weighted by its respective probability.

