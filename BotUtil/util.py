from audioop import reverse
import os
from scipy.stats import entropy
from json import load,dump
from tqdm import tqdm
ALLOWED_WORDS = os.path.join(os.path.dirname(__file__),'../data/allowed_words.txt')
FREQ_MAP = os.path.join(os.path.dirname(__file__),'../data/freq_map.json')
NUM_PATTERNS = 3**5

class Pattern(object):
    NOT_EXIST = 0
    WRONG_PLACE = 1
    CORRECT = 2
    def __init__(self,word):
        self.word = word
        
    def get_pattern(self,target):
        '''
            return pattern on self.word|target
        '''
        pattern = []
        for i,ch in enumerate(self.word):
            if ch not in target:
                pattern.append(Pattern.NOT_EXIST)
            elif self.word[i] == target[i]:
                pattern.append(Pattern.CORRECT)
            else:
                pattern.append(Pattern.WRONG_PLACE)
        return pattern
    
    def set_pattern(self,pattern):
        self.pattern = pattern
        
    def guess(self,target,pattern=None):
        '''
            Boolean. 
            Return True if pattern on self.word|target matches the current.
            else False.
        '''
        if pattern == None:
            pattern = self.pattern
        target_pattern = self.get_pattern(target)
        for i,p in enumerate(target_pattern):
            if p != pattern[i]:
                return False
        return True
    
    def hit(self):
        if self.pattern != None:
            idx = int(''.join([str(_) for _ in self.pattern]),3)
            if idx == int('22222',3):
                return True
        return False
    
class DataSet(object):
    def __init__(self,path = FREQ_MAP):
        freq_map = open(path,'r')
        self.words = load(freq_map)
    
    def all_words(self):
        return self.words.keys()
    
    def filter(self,pattern,words=None):
        '''
            remove word that does not match the pattern from words, 
            return left words.
        '''
        if words != None:
            self.words = words            
        new_words = list()
        res = dict()
        pr_sum = 0.0
        print("** Filtering dataset on pattern {}... **".format(pattern))
        for word,pr in tqdm(self.words.items()):
            if pattern.guess(word) == True:
                new_words.append(word)
                pr_sum += pr
        for word in new_words:
            res[word] = self.words[word] / pr
        self.words = res
        return res

    def distribution_of_every_pattern(self,word):
        '''
            Calculate the distribution on every pattern with given word (pattern is word|target).
            The result is stored in a list, [idx] -> pr
        '''
        distribution = [0]*NUM_PATTERNS
        pattern = Pattern(word)
        for target in self.words:
            p = pattern.get_pattern(target)
            idx = int(''.join([str(_) for _ in p]),3)
            distribution[idx] += self.words[target]
        return distribution
    
    def entropy(self,word):
        '''
            return entroy on the distribution of every pattern
        '''
        return entropy(self.distribution_of_every_pattern(word))
    
class WordleBot(object):
    def __init__(self):
        self.dataset = DataSet()
    
    def next(self,pattern=None,first_round=False):
        '''
            return candidates of next word on current dataset.
            if pattern is provided, do filter on current dataset
        '''
        if pattern != None:
            self.dataset.filter(pattern)
        if first_round == True:
            candidates = load(open(os.path.join(os.path.dirname(__file__),'../data/first_candidates'),'r'))
            candidates = dict(sorted(candidates.items(),key=lambda item: item[1],reverse=True))
            return candidates
            
        candidates = dict()
        print("** Calculating distribution of patterns on every word... **")
        for word in tqdm(self.dataset.words.keys()):
            candidates[word] = self.dataset.entropy(word)
        candidates = dict(sorted(candidates.items(),key=lambda item: item[1],reverse=True))
        return candidates
    
    
if __name__ == '__main__':
    '''
        To calculate candidates of first round and cache them in file, since it costs a lot of time to finish calculation.
    '''
    bot = WordleBot()
    # store first round data
    f = open(os.path.join(os.path.dirname(__file__),'../data/first_candidates'),'w')
    candi = bot.next(first_round=False)
    dump(candi,f)
        


    