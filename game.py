from BotUtil import WordleBot, Pattern, DataSet
from getpass import getpass

class Game:
    def __init__(self):
        self.dataset = DataSet()
        
    def get_secret(self):
        while True:
            self.target = getpass("input secret word of length 5: ")
            if self.target not in self.dataset.all_words():
                print("Not a valid word. Type a newone!")
            else:
                print("Secret got!\nGame is starting...")
                break
        
    def get_pattern(self,word):
        pattern = Pattern(word)
        p = pattern.get_pattern(self.target)
        pattern.set_pattern(p)
        return pattern
    
    def show_pattern(self,pattern):
        print("\n***\npattern is: ",end='')
        for p in pattern.pattern:
            print("{}".format(p),end=' ')
        print("\n***\n")
    
    def get_next_guess(self):
        word = input("input next guess: ")
        return word
    
def main():
    game = Game()
    game.get_secret()
    bot = WordleBot()
    first_round=True
    pattern = None
    while True:
        candidates = bot.next(pattern = pattern,first_round=first_round)
        first_round = False
        print(list(candidates.items())[:10])
        word = game.get_next_guess()
        pattern = game.get_pattern(word)
        game.show_pattern(pattern)
        if pattern.hit() == True:
            print("Correct!")
            break
        # game.show_pattern(pattern)
    
main()