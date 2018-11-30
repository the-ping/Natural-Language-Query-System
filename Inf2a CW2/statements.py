# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements


def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    #POScat = ["P", "A", "I", "N", "T"]

    def __init__(self):
        self.list = []

    def add(self, stem, cat):
        add(self.list, (stem, cat))


    def getAll(self, cat):
        stemlist = []
        for pair in self.list:
            if cat in pair:
                add(stemlist, pair[0])
        return stemlist



class FactBase:
    #"stores unary and binary relational facts"

    def __init__ (self):
        self.listU = []
        self.listB = []

    def addUnary(self, pred, e1):
        add(self.listU, (pred, e1))

    def addBinary(self, pred, e1, e2):
        add(self.listB, (pred, e1, e2))

    def queryUnary(self, pred, e1):
        for i in self.listU:
            if (pred, e1) in self.listU:
                return True
            else:
                return False

    def queryBinary(self, pred,e1, e2):
        for i in self.listB:
            if (pred,e1, e2) in self.listB:
                return True
            else:
                return False



import re
from nltk.corpus import brown



def verb_stem(s):
    #"extracts the stem from the 3sg form of a verb, or returns empty string"

    btw = set(brown.tagged_words())

    res1 = re.match('[A-Z]*[a-z]+([^sxyzaeiou]|^(sh)|^(ch))s$',s) #eats, tells, shows
    res2 = re.match('[A-Z]*[a-z]+[aeiou]ys$',s) #pays, buys
    res3 = re.match('[A-Z]*[a-z]+[^aeiou]ies$',s) #flies, tries, unifies
    res4 = re.match('[^aeiou]ies$',s) #dies, lies, ties
    res5 = re.match('[A-Z]*[a-z]+(o|x|ch|sh|ss|zz)es$',s) #goes, boxes, attaches, fizzes, dresses
    res6 = re.match('[A-Z]*[a-z]+([^s]se)|([^z]ze)s$',s) #loses, dazes, lapses
    res7 = re.match('has$',s) #has
    res8 = re.match('[A-Z]*[a-z]+([^iosxz]|^(ch)|^(sh))es',s) #likes, hates, bathes

    if res1:
         n3s = s[0:-1]

    elif res2:
        n3s = s[0:-1]

    elif res3:
        n3s = s[0:-3] + 'y'

    elif res4:
        n3s = s[0:-1]

    elif res5:
        n3s = s[0:-2]

    elif res6:
        n3s = s[0:-1]

    elif res7:
        n3s = 'have'

    elif res8:
        n3s = s[0:-1]

    else:
        return ''


    if (s, 'VBZ') or (n3s, 'VB') in btw:
        return n3s




def add_proper_name (w,lx):
    #"adds a name to a lexicon, checking if first letter is uppercase"
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg


# End of PART A.

