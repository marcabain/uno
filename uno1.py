# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 22:03:41 2018

@author: Teri
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
#put cards in 3 different hands, this is easy to change how many players
numplayers=3
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
    
#this card stats the game
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
wildcolor=''  #empty because it gets filled in when one is played my human or com.
while discard[-1]=={'color':'black','face':'draw4'}:
    deck.append(discard[-1])
    del discard[-1]
    random.shuffle(deck)  
    discard.append(deck.pop())
if discard[-1]=={'color':'black','face':'wild'}:
    printgamestate(discard,hand,numplayers)
    legalcolor=False
    while not legalcolor:
        wildcolor=input('choose a color: ')
        legalcolor=wildcolor in color 
if discard[-1]['face']=='draw2':
    printgamestate(discard,hand,numplayers)
    hand[0].append(deck.pop())
    hand[0].append(deck.pop())
    print('player 1 drew 2 cards')
    i=1
if discard[-1]['face']=='skip': 
    printgamestate(discard,hand,numplayers)
    print('player 1 got skipped')
    i=1
if discard[-1]['face']=='reverse':
    clockwise=False
 
skipcard=False    
drawcards=0
gameover=False  #game is not over until we say it is, when someone is out of cards
while not gameover:
    if i == 0:  #this is the human, at [0]
        printgamestate(discard,hand,numplayers)
        cardlegal=False   #I haven't chosen a card yet
        while not cardlegal:
            cardtoplay=input('choose a card: ')
            try:
                cardtoplay=int(cardtoplay)  #cardtoplay my cards to choose from
                if cardtoplay not in range(1,len(hand[i])+2):  #if number was wrong
                    print ('enter valid number, 1-' + str(len(hand[i])+1))
                elif cardtoplay==len(hand[i])+1:  
                    hand[i].append(deck.pop())  
                    cardlegal=True
#lines 91 is just turning the string input by the user into a number
#The elif statement is checking if number given is the "draw a card"
#option since we list out the cards and then make that choice next
# (so it is alwyas len(hand[i]+1))
                    print ("you drew: " + printcard(hand[i][-1]))
                    if canplay(discard[-1],hand[i][-1],wildcolor):
                        print ("you played it")
                        if hand[i][-1]['color']=='black':
                            legalcolor=False
                            while not legalcolor:
                                 wildcolor=input('choose a color: ')
                                 legalcolor=wildcolor in color  
#line 106 the wildcolor is only the colors in the list color at the start of code
#92-102 is only if I did not have a card to play, and the card that I drew
#was a wild and that was played, below 107-110 is if I drew a non wild card that could
#be played                                
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
                elif canplay(discard[-1],hand[i][cardtoplay-1],wildcolor):
                    cardlegal=True  #goes to this step if card in hand can play
                    if hand[i][cardtoplay-1]['color']=='black':
                        legalcolor=False
                        while not legalcolor:
                            wildcolor=input('choose a color: ')
                            legalcolor=wildcolor in color
#line 121 how to choose a legal color, blue, yellow, red or green from list at beginning
#lines 115-116 if I had a wild card to play in my hand and chose that card  
#below this is if I do not play a wild card                           
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
                    discard.append(hand[i][cardtoplay-1])
                    del hand[i][cardtoplay-1]
                else:
                    print("pick different card")
            except ValueError:
                if cardtoplay=="quit":
                    sys.exit()  #when we run the game we can stop it
                print("invalid number")
#lines 85 to 130 is for the human player              
    else:
        complayedcard=False
        j=0  #j is the card in the hand of com.player
        while j<len(hand[i]):  #we inerate through hand to find legal card to play
            if canplay(discard[-1],hand[i][j],wildcolor):
                print ('complayer ' + str(i+1) + ' played '+ printcard(hand[i][j]))
                if hand[i][j]['color']=='black':
                    wildcolor='blue'
                    print ('complayer ' + str(i+1) + ' chose blue ')
#137-143 if com. plays a wild they choose blue
#below this is if the com. plays a no wild color                   
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
        if not complayedcard:
            print ('complayer ' + str(i+1) + ' drew a card ')
            hand[i].append(deck.pop())
            if canplay(discard[-1],hand[i][-1],wildcolor):
                print ('complayer ' + str(i+1) + ' played '+ printcard(hand[i][-1]))
                if hand[i][-1]['color']=='black':
                    wildcolor='blue'
                    print ('complayer ' + str(i+1) + ' chose blue ')
#lines 154 if com drew a card
#line 157 if the card that was drawen was a wild                   
#below is if the com. drew a card that was not wild, but was playable                   
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

    if len(hand[i])==0:
        gameover=True  
        print ('player won')
    elif len(hand[i])==1:
        print ('UNO!')
    if clockwise:
        i=(i+1)%numplayers   #this is how we go from hand[0]and to the other players
                            #and back again to hand [0] 
    else:
        i=((i-1)+numplayers)%numplayers                      
        
    if drawcards>0:
        for j in range(0,drawcards):
            hand[i].append(deck.pop())
        print('player ' + str(i+1)+ ' drew ' + str(drawcards) + ' cards')
        drawcards=0
        if clockwise:
            i=(i+1)%numplayers   
        else:
            i=((i-1)+numplayers)%numplayers  
    
 
    if skipcard:
        if clockwise:
            i=(i+1)%numplayers   
        else:
            i=((i-1)+numplayers)%numplayers  
        skipcard=False
        
        
    
        

                  
            #for card in (hand[i]):
             #   if canplay(discard[-1],card,wildcolor):
   # printgamestate(discard,hand,numplayers)
                
   # gameover=True
    
    
#we are asking hand[0] me/human what card they want to play
#nested loop that goes with the fuction above to know what is a playable card
#I did the try block, because at first it said key error
#it will always be discard[-1]to show what card is in play
#hand[0]/me,cardtoplay-1, that is what card that I will play
#I did [cardtoplay-1]because we number the cards1to7 but the program
    #does 0 to6

#cardtoplay=input('choose a card: ')
#try:
 #   cardtoplay=int(cardtoplay)
#except:
 #   print("invalid number")
#if canplay(discard[-1],hand[0][cardtoplay-1],""):
 #   print("legal")
#else:
 #   print("illegal")
    
#while the game isn't over
 # for each player in the game
  #  if it is player 0
   #   print the game state and prompt for a card
    #  if given a legal card, append it to the discard and remove it from their hand
     # if it was a black card, prompt for the color choice and set "wildcolor" to it
    #if it is not player 0
     # select the first playable card in their hand and play it
      #if it was a black card
       # select a random color and print it to the screen, set "wildcolor" to it
      #print the card played so the human player can see what happened
    #if the card was a reverse, reverse the direction of the loop
    #if the card was a skip, move two players forward
    #if the card wasn't a skip, move one player forward
    #if the player has 1 card, print "Uno!"
    #If the player has 0 cards, set a boolean to state the game is over and end the while loop
