# check

This repository contains a simple minimax AI for the game of [checkers](https://en.wikipedia.org/wiki/Draughts). The minimax algorithm is implemented using Alpha-beta pruning in order to cut out unnecessary branches during decision tree exploration. Two simple heuristic functions are provided: one that accounts only for the number and types of pieces, and one that also weighs piece positions (the further into the opponent's side of the board the piece is, the more valuable it is).

There is a simple TUI for playing the game against the computer; run it with `python game.py`. Run `python game.py --help` for additional commandline options.