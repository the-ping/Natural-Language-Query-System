# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

"""
lx = Lexicon()
lx.add('Mary', 'P')
lx.add('like', 'T')
lx.add('orange', 'A')
lx.add('orange', 'N')
lx.add('fly', 'I')
lx.add('fly', 'N')
lx.add('a', 'AR')
lx.add('and', 'AND')
lx.add('sheep', 'N')
lx.add('fish', 'T')



print(tag_word(lx, 'Mary'))
print(tag_word(lx, 'like'))
print(tag_word(lx, 'likes'))
print(tag_word(lx, 'orange'))
print(tag_word(lx, 'oranges'))
print(tag_word(lx, 'a'))
print(tag_word(lx, 'and'))
print(tag_word(lx, 'fly'))
print(tag_word(lx, 'flies'))
print(tag_word(lx, 'sheep'))
print(tag_word(lx, 'fish'))
print(tag_word(lx, 'fishes'))

wds = ['Mary', 'like', 'likes', 'orange', 'oranges', 'a', 'and', 'fly', 'flies', 'sheep', 'fish', 'fishes']

------------

lx = Lexicon()
lx.add('who', 'WHO')
lx.add('is', 'BEs')
lx.add('crazy', 'A')
lx.add('does', 'DOs')
lx.add('John', 'P')
lx.add('like', 'T')
lx.add('?', '?')
lx.add('kill', 'I')
lx.add('duck', 'N')
lx.add('Jack', 'P')
lx.add('room', 'N')
lx.add('does', 'DOs')
lx.add('like', 'T')


ww = ['who', 'is', 'crazy', '?']
ww2 = ['who', 'does', 'John', 'like', '?']
ww3 = ['which', 'duck', 'kills', '?']
ww4 = ['which', 'room', 'does', 'Jack', 'likes', '?']

"""

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    nn = {}
    nns = {}
    up_list = set()
    with open("sentences.txt", "r") as f:
        for line in f:
            for word in set(line.split()):
                res1 = re.match('[a-zA-Z]+\|NN$', word)
                res2 = re.match('[a-zA-Z]+\|NNS$', word) #delivers|NNS
                if res1:
                    nn[word[0:-3]] = word[-2:]

                if res2:
                    nns[word[0:-4]] = word[-3:]


    for word_s, tag_s in nns.iteritems():
        for word, tag in nn.iteritems():
            if word_s == word:
                    up_list.add(word)
    return up_list


unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    #""extracts the stem from a plural noun, or returns empty string""


        if s in unchanging_plurals_list:
            return s

        elif re.match('[a-zA-Z]*men', s):
            return s[:-3] + 'man'

        else:
            res1 = re.match('([A-Z]*[a-z]+[^s|x|y|z|ch|sh|a|e|i|o|u])s$', s)  # eats, tells, shows
            res2 = re.match('[A-Z]*[a-z]+[a|e|i|o|u]ys$', s)  # pays, buys
            res3 = re.match('[a-z][a-z]ies$', s)  # flies, tries, unifies
            res4 = re.match('[^a|e|i|o|u]ies$', s)  # dies, lies, ties
            res5 = re.match('[A-Z]*[a-z]+(o|x|ch|sh|ss|zz)es$', s)  # goes, boxes, attaches, fizzes, dresses
            res6 = re.match('[A-Z]*[a-z]+([^s]se)|([^z]ze)s$', s)  # loses, dazes, lapses
            res8 = re.match('[A-Z]*[a-z]+[^i|o|s|x|z|ch|sh]es', s)  # likes, hates, bathes

            if res1:
                return s[0:-1]

            elif res2:
                return s[0:-1]

            elif res3:
                return s[0:-3] + 'y'

            elif res4:
                return s[0:-1]

            elif res5:
                return s[0:-2]

            elif res6:
                return s[0:-1]

            elif res8:
                return s[0:-1]

            else:
                return ''



def tag_word (lx,wd):
    #""returns a list of all possible tags for wd relative to lx""
    #btw = set(brown.tagged_words())

    P1 = ['P', 'A'] #solos
    P2 = ['I', 'T'] #verbs

    taglist = set()

    if wd in function_words:
        for k, v in function_words_tags:
            if k == wd:
                taglist.add(v)

    for p in P1:
        if wd in lx.getAll(p):
            taglist.add(p)


    stem_v = verb_stem(wd)
    for i in P2:
        if stem_v in lx.getAll(i):
            taglist.add(i + 's')
        if wd in lx.getAll(i):
            taglist.add(i + 'p')


    stem_n = noun_stem(wd)
    if wd in lx.getAll('N'):
        taglist.add('Ns')

    if stem_n != '':
        if stem_n == wd:
            taglist.add('Ns')
            taglist.add('Np')
        else:
            taglist.add('Np')


    return list(taglist)



def tag_words (lx, wds):
    #""returns a list of all possible taggings for a list of words""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]


# End of PART B.