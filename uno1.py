# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:03:41 2018

@author: 
"""
import sys
import random
#create a deck of cards
color=['red','blue','green','yellow']
face=['0','1','2','3','4','5','6','7','8','9','skip','reverse','draw2']

deck=[]
cards={}
#deck of cards is a list of cards as dictionary
for c in color:
    for f in face:
        card={'color':c,'face':f}
        deck.append(card)
        if f !='0':
            deck.append(card)
#add wild cards         
for i in range(0,4):
    deck.append({'color':'black','face':'wild'})
    deck.append({'color':'black','face':'draw4'})

#print(len(deck))
#shuffle deck
random.shuffle(deck)   
# create player hands
#put cards in 5 different hands, this is easy to change how many players
numplayers=5
hand=[]
#initalize hand list to empty hand
for n in range(0,numplayers):
    hand.append([])
#deal cards in to hands
for i in range(0,7):#7 cards perhand
    for j in range(0,numplayers):  #j is the players, i is the cards you pop7 cards
        hand[j].append(deck.pop())
#for h in range(0,numplayers):
    #print(hand[h])
    
#this card starts the game
discard=[]
discard.append(deck.pop())
#this function tells you how the card will look when printed
def printcard(c):
    return (c['color'] + " " + c['face'])
#this function prints game state
def printgamestate(discard,hand,numplayers):
    print("discard = " + printcard(discard[-1]))

    for i in range(1,numplayers):
        print('num of cards in player'+ str(i+1)+ ' = ' + str(len(hand[i])))
    printhand(hand)   #this prints how many cards each player has
    
#function for printing my hand[0], and if I have to draw a card
    #so I can choose what card by just picking a number
def printhand(hand):
    print ("my hand")
    cardnum=1
    for i in (hand[0]):
        print("  "+ str(cardnum),printcard(i))
        cardnum=cardnum+1
    print("  "+ str(len(hand[0])+1),"draw a card")
    #we needed to say draw a card, if I do not have a legal card to play
        
#this is a function of rules when you can play on the discard pile
def canplay(discard, card, wildcolor):
    if card['color']==discard['color']:
        return True
    if card['face']==discard['face']:
        return True
    if card['color']=='black':
        return True
    if discard['color']=='black' and card['color']==wildcolor:
        return True
    return False
#discard.append({'color':'red','face':'reverse'})
clockwise=True
i=0   #start with human player
wildcolor=''  #empty because it gets filled in when one is played by human or com.

#if 1st card is a draw4, we put back into deck and shuffle to restart
while discard[-1]=={'color':'black','face':'draw4'}:
    deck.append(discard[-1])
    del discard[-1]
    random.shuffle(deck)  
    discard.append(deck.pop())
#if 1st card is a wild, player 1 chooses a color and begins game
if discard[-1]=={'color':'black','face':'wild'}:
    printgamestate(discard,hand,numplayers)
    legalcolor=False
    while not legalcolor:
        wildcolor=input('choose a color: ')
        legalcolor=wildcolor in color 
#if 1st card is a draw2, then player 1 draws to and game goes to player 2
if discard[-1]['face']=='draw2':
    printgamestate(discard,hand,numplayers)
    hand[0].append(deck.pop())
    hand[0].append(deck.pop())
    print('player 1 drew 2 cards')
    i=1    #player 2 plays
#if 1st card is a skip, game will skip player 1, and go to player 2
if discard[-1]['face']=='skip': 
    printgamestate(discard,hand,numplayers)
    print('player 1 got skipped')
    i=1
#if 1st card is a reverse, the game will go 1,3,2
if discard[-1]['face']=='reverse':
    clockwise=False
 
skipcard=False      #set to False, because we haven't played yet
drawcards=0         #set to 0, because a draw card hasn't been played yet
gameover=False  #game is not over until we say it is, when someone is out of cards
print ("Let's play Uno with " + str(numplayers) + " players, type 'quit' to exit game")
while not gameover:
    if len(deck)==0:    #119-126, if deck is empty, put discard back to deck and shuffle
        print ('deck is empty, we will shuffle discard into deck')
        topdiscard=discard[-1]
        del discard[-1]     #we need to leave top card for discard pile
        deck=discard.copy()
        discard.clear()
        discard.append(topdiscard)
        random.shuffle(deck)
    if i == 0:  #this is the human, at [0]
        printgamestate(discard,hand,numplayers)
        cardlegal=False   #I haven't chosen a card yet
        while not cardlegal:
            cardtoplay=input('choose a card: ')#this turns the string input by the user into a number
            try:
                cardtoplay=int(cardtoplay)  #cardtoplay my cards to choose from
                if cardtoplay not in range(1,len(hand[i])+2):  #if number was wrong
                    print ('enter valid number, 1-' + str(len(hand[i])+1))
#138-161 if I drew a card, and if it is playable it will say I drew a card and I played it
#if I did not draw a playable card, it would go to next player
                elif cardtoplay==len(hand[i])+1:  
                    hand[i].append(deck.pop())   #card I draw goes in to hand
                    cardlegal=True
                    print ("you drew: " + printcard(hand[i][-1]))
                    if canplay(discard[-1],hand[i][-1],wildcolor):
                        print ("you played it") #says whet card I drew I played
                        if hand[i][-1]['color']=='black':  #if it is black it is wild
                            legalcolor=False
                            while not legalcolor:
                                 wildcolor=input('choose a color: ')
                                 legalcolor=wildcolor in color  
#wildcolor is in the color list at the beginning
                        else:
                            wildcolor=''  #if there is no wild card played
                        if hand[i][-1]['face']=='draw2':
                            drawcards=2
                        elif hand[i][-1]['face']=='draw4':
                            drawcards=4
                        elif hand[i][-1]['face']=='skip':
                            skipcard=True
                        elif hand[i][-1]['face']=='reverse':
                            clockwise=not clockwise
                        discard.append(hand[i][-1])  #card went on discard pile
                        hand[i].pop()  #card was poped out of hand
#line 163-181 if I didn't have to draw a card, and played a card in my hand                        
                elif canplay(discard[-1],hand[i][cardtoplay-1],wildcolor):
                    cardlegal=True  #goes to this step if card in hand can play
                    if hand[i][cardtoplay-1]['color']=='black':
                        legalcolor=False
                        while not legalcolor:
                            wildcolor=input('choose a color: ')
                            legalcolor=wildcolor in color                         
                    else:
                        wildcolor=''  #if there is no wild card played
                    if hand[i][cardtoplay-1]['face']=='draw2':
                        drawcards=2
                    elif hand[i][cardtoplay-1]['face']=='draw4':
                        drawcards=4
                    elif hand[i][cardtoplay-1]['face']=='skip':
                        skipcard=True 
                    elif hand[i][cardtoplay-1]['face']=='reverse':
                        clockwise=not clockwise
                    discard.append(hand[i][cardtoplay-1])  #puts card I chose into discard
                    del hand[i][cardtoplay-1]     #this delets the card I play from my hand
                else:
                    print("pick different card")
            except ValueError:
                if cardtoplay=="quit":
                    sys.exit()  #when we run the game we can stop it
                print("invalid number")
#lines 127 to 183 is for the human player              
    else:       # if computer is playing
        complayedcard=False
        j=0  #j is the card in the hand of com.player
        while j<len(hand[i]):  #we inerate through hand to find legal card to play
            if canplay(discard[-1],hand[i][j],wildcolor):
                print ('complayer ' + str(i+1) + ' played '+ printcard(hand[i][j]))
                if hand[i][j]['color']=='black':
                    wildcolor=color[random.randint(0,3)]
                    print ('complayer ' + str(i+1) + ' chose ' + wildcolor)
#line 194 prints what com. player plays, line 195 if they play a wild, they choose a random
#color, from the list of colors at the beginning of code. we print that too, so
#so we know what color to play
#line 194-215 if computer plays a playable card
                else:
                    wildcolor=''  #close out wild if one was not played
                if hand[i][j]['face']=='draw2':
                    drawcards=2
                elif hand[i][j]['face']=='draw4':
                    drawcards=4  
                elif hand[i][j]['face']=='skip':
                    skipcard=True
                elif hand[i][j]['face']=='reverse':
                    clockwise=not clockwise
                discard.append(hand[i][j])
                del hand[i][j]
                complayedcard=True
                break  #stop looking for legal cards
            j+=1  #inerate though cards in hand
#lines 218 to 237 is if com. player had to draw a card
        if not complayedcard:
            print ('complayer ' + str(i+1) + ' drew a card ')
            hand[i].append(deck.pop())
            if canplay(discard[-1],hand[i][-1],wildcolor):
                print ('complayer ' + str(i+1) + ' played '+ printcard(hand[i][-1]))
                if hand[i][-1]['color']=='black':
                    wildcolor=color[random.randint(0,3)]
                    print ('complayer ' + str(i+1) + ' chose ' + wildcolor)                              
                else:
                    wildcolor=''
                if hand[i][-1]['face']=='draw2':
                    drawcards=2
                elif hand[i][-1]['face']=='draw4':
                    drawcards=4 
                elif hand[i][-1]['face']=='skip':
                    skipcard=True
                elif hand[i][-1]['face']=='reverse':
                    clockwise=not clockwise
                discard.append(hand[i][-1])  #card went on discard pile
                hand[i].pop()

    if len(hand[i])==0:    #if any hand has 0 cards then the game is over
        gameover=True  
        print ('player ' + str(i+1) + ' won')    #prints after last card in hand is played
    elif len(hand[i])==1:
        print ('UNO!')      #prints after 2nd to last card is played
    if clockwise:
        i=(i+1)%numplayers   #this is how we go from hand[0]and to the other players
                            #and back again to hand [0] 
    else:
        i=((i-1)+numplayers)%numplayers    #if we play a reverse and we go 3,2,1                    
        
    if drawcards>0:             #if you play a draw card 
        for j in range(0,drawcards):
            hand[i].append(deck.pop())  #we print out who had to draw
        print('player ' + str(i+1)+ ' drew ' + str(drawcards) + ' cards')
        drawcards=0      #we set it back to 0 after it is done
        if clockwise:
            i=(i+1)%numplayers   
        else:
            i=((i-1)+numplayers)%numplayers  
    
 
    if skipcard:       #if we play a skip card
        if clockwise:
            i=(i+1)%numplayers   
        else:
            i=((i-1)+numplayers)%numplayers  
        skipcard=False       #we set it back to false once it is done
        
        
    
        

                  
    
