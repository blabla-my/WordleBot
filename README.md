# WordleBot

Algorithm to solve the wordle game.

About wordle game: https://www.nytimes.com/games/wordle/index.html

### Algorithm
From 3Blue1Black's idea of entropy:

https://www.youtube.com/watch?v=v68zYyaEmEA

I implemented my own version as coding practice.

### usage
```
git clone https://github.com/blabla-my/WordleBot.git
cd WordleBot
python3 -m pip install -r requirements.txt
python3 game.py 
```

### Interactive mode
You can use this wordlebot to solve games hold by third party such as https://www.nytimes.com/games/wordle/index.html

Just use the interactive mode, wordlebot will get the pattern of each round from your input.
```
python3 game.py --interactive
```

You can input a string of number to represent the pattern. For example:

`Black Black Yellow Green Black == 00120`

Have fun playing with my wordlebot (^ ^)!
