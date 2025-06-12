This project builds an intelligent bot to play Heads-Up Liar’s Dice, using opponent modeling and probability to evaluate the best move in any situation. The engine dynamically builds and updates range estimates based on bidding behavior and computes expected win probabilities for each possible action.

🔍 Features
✅ Range Construction: After each bid, the bot updates a probabilistic model of the opponent’s possible hands

✅ Move Evaluation:

Liar: Calculates the expected win chance of calling a bluff

Calza: Computes odds of an exact match (optional toggle)

Bid: Simulates the opponent’s most likely responses based on their estimated range to determine the optimal next bid

✅ Performs best in later-game situations (e.g. bids of 2 or more of a face), where recursion over possible future outcomes provides deeper strategic insight

🧠 Strategy Engine
Uses Bayesian-style reasoning to model opponent hand distributions

Evaluates the expected value of each legal move

Employs recursive analysis of bidding trees to simulate realistic gameplay dynamics

💡 Concepts Used
Probability theory & opponent modeling

Range-based decision-making inspired by poker AIs

Recursive simulation of game trees

🛠️ Tech Stack
Python (numpy, random)

Custom engine to simulate dice rolls, bids, and opponent responses

