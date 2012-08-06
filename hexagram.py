import random
from recipe576707 import CMWC

try:
    rand = random.SystemRandom()
except:
    rand = random
    rand.seed()
    print "System randomness is not available on your computer."
    print "Using Python random module."

hvals = [
2, 24, 7, 19, 15, 36, 46, 11,
16, 51, 40, 54, 62, 55, 32, 34,
8, 3, 29, 60, 39, 63, 48, 5,
45, 17, 47, 58, 31, 49, 28, 43,
23, 27, 4, 41, 52, 22, 18, 26,
35, 21, 64, 38, 56, 30, 50, 14,
20, 42, 59, 61, 53, 37, 57, 9,
12, 25, 6, 10, 33, 13, 44, 1
]
# The index is the binary value of the hexagram, so hvals[0]
# is "Hexagram 2", which consists of 6 broken (yin) lines.
  
############################################
  
def zeroto4(n):
    if n: return n
    else: return 4
    
def umilfoil(stalks):
    pile1 = rand.randint(1, stalks-1)
    pile2 = stalks - pile1
    # divides the milfoil into two piles
    firsttake = 1
    pile1 -= firsttake
    secondtake = zeroto4(pile2 % 4)
    pile2 -= secondtake
    thirdtake = zeroto4(pile1 % 4)
    pile1 -= thirdtake
    return pile1+pile2
        
def milfoilline():
    stalks = 50-1
    #Take 50 stalks of milfoil; remove one for unity
    for i in range(3):
        stalks = umilfoil(stalks)
##        print stalks # for testing purposes
    return stalks/4

def ucoin():
    if rand.getrandbits(1):
        return 3
    else:
        return 2
    
def coinline():
    return ucoin() + ucoin() + ucoin()

def line(value):
    """One line has the form (Yin or Yang, Static or Changing). Yin and Static
have values "False", Yang and Changing have values "True"."""
    if value == 6:
        return (False, True)
    if value == 7:
        return (True, False)
    if value == 8:
        return (False, False)
    if value == 9:
        return (True, True)


def generatehex(coinmethod=False):
    boolhex = []
    if coinmethod:
        while len(boolhex) < 6:
            boolhex.append(line(coinline()))
            # The first line appended to the hexagram is line 0
    else:
        while len(boolhex) < 6:
            boolhex.append(line(milfoilline()))
            
    return boolhex

def getbinvalue(boolhex):
    sum = 0
    for i in range(len(boolhex)):
        sum += boolhex[i][0] << i
    return sum

def output(boolhex):
    print "\nHexagram %d" % hvals[getbinvalue(boolhex)]
    
    for L in range((len(boolhex)-1), -1, -1):
        if boolhex[L][0]: #If the line value is odd
            print "---------------"
        else:
            print "-----     -----"
    print "\n"
    
    static = True
    for i in range(len(boolhex)):
        if boolhex[i][1]:
            print "Line " + str(i + 1) + " is a moving line."
            static = False
    if static:
        print "No changing lines."
    return not static # will return True if the hexagram changes


def changehex(boolhex):
    for i in range(len(boolhex)):
        if boolhex[i][1]: # is True
            boolhex[i] = (not boolhex[i][0], not boolhex[i][1])
    return boolhex


def session():
    user_input = raw_input("Please type your question: ")
    boolhex = generatehex()
    if output(boolhex):
        print "\nThe following is the hexagram after the change:"
        output(changehex(boolhex))
    filler = raw_input("\nAny key to exit.\n")

if __name__ == '__main__':
    print "This program is a plain text implementation of the Yijing.\n"
    session()
        
