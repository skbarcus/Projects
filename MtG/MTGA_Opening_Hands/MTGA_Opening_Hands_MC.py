from matplotlib import pyplot as plt
import numpy as np
import random
import collections
#from collections import Counter

decks = []                  #List holding decks each with a differnt land count (from no lands to all lands).
deck_info = []              #List for classes that represent each deck with a different land count.
nlands = 15                 #Number of lands in deck to be studied.
deck_size = 40              #Number of cards in deck.
nhands = 1000000                  #Total number of sample hands to draw.
nopener = 7                 #Number of cards to draw for the opening hand.
opening_lands = []          #List for the number of lands in each normal opening hand.
bo1_opening_lands = []      #List for the number of lands in each MtGA Bo1 opening hand.

def draw(lands = 17, n = 1):
    drawn_cards = random.sample(decks[lands],n)
    return drawn_cards

def print_deck_stats(argument):
    deck = argument
    print("This deck has %d cards. %d lands and %d nonlands. %.3f%% of the deck is lands." % (deck.deck_size,deck.lands,deck.nonlands,deck.land_frac*100))

class deck_stats:
    def __init__(self, lands = 17):
        self.lands = lands
        self.deck_size = deck_size
        self.nonlands = self.deck_size - self.lands
        self.land_frac = self.lands/self.deck_size
        #print("This deck has %d cards. %d lands and %d nonlands." % (self.deck_size,self.lands,self.nonlands))

#Create deck_size+1 number of decks containing zero lands through only lands.
for i in range(0,deck_size+1):
        lands = i
        nonlands = deck_size - i
        decks.append([])
        #print("lands = ",lands," nonlands = ",nonlands)
        for j in range(0,lands):
            decks[i].append("land")
        for j in range(0,nonlands):
            decks[i].append("nonland")

#Initialize a class for each of the decks with a different number of lands.
for i in range(0,deck_size+1):
    deck_info.append(deck_stats(i))

#Print the stats for the chosen deck.
print_deck_stats(deck_info[nlands])

#print("decks[0] = ",decks[0])
#print("decks[1] = ",decks[1])
#print("decks[40] = ",decks[40])
#print("deck = ",deck)

#test_hand = draw(17,7)
# print("Sample starting hand. ",test_hand)
# l = collections.Counter(test_hand)
# print(l)
# print(l["land"])
# print(l["nonland"])

total_lands = 0
bo1_total_lands = 0
for i in range(0,nhands):
    #Draw normal MtG hand.
    hand = draw(nlands,nopener)
    #Store the resulting numbers of lands and nonlands in the hand in the distributions counter.
    dist = collections.Counter(hand)
    #Store the number of lands in the opening hand in a list to be used for the histogram later.
    opening_lands.append(dist["land"])
    #Keep track of the total number of lands drawn over all hands for later average calculations.
    total_lands = total_lands+dist["land"]
    #print(dist["land"])

    #Draw best of one hand in the style of MtGA.
    bo1_hand1 = draw(nlands,nopener)
    #print("bo1_hand1",bo1_hand1)
    bo1_dist1 = collections.Counter(bo1_hand1)
    #Calculate the fraction of lands in the first bo1 hand drawn.
    land_frac1 = bo1_dist1["land"]/nopener
    bo1_hand2 = draw(nlands,nopener)
    #print("bo1_hand2",bo1_hand2)
    bo1_dist2 = collections.Counter(bo1_hand2)
    #Calculate the fraction of lands in the second bo1 hand drawn.
    land_frac2 = bo1_dist2["land"]/nopener
    #print("land_frac1 = %.3f land_frac2 = %.3f" % (land_frac1,land_frac2))
    #Calculate how far from the deck's average land fraction each of the two opening bo1 hands was.
    d1 = abs(land_frac1-deck_info[nlands].land_frac)
    d2 = abs(land_frac2-deck_info[nlands].land_frac)
    #print("d1 = ",d1," d2 = ",d2)
    #Choose to keep the hand with a mana ratio closest to that of the deck.
    if d1 <= d2:
        bo1_opening_lands.append(bo1_dist1["land"])
        bo1_total_lands = bo1_total_lands+bo1_dist1["land"]
    else:
        bo1_opening_lands.append(bo1_dist2["land"])
        bo1_total_lands = bo1_total_lands+bo1_dist2["land"]

#print("b01_opening_lands = ",bo1_opening_lands)

#Print the stats for a normal MtG hand.
total_sample = collections.Counter(opening_lands)
print("total_sample ",total_sample)
print("Average lands in opening hand = %.3f."% (total_lands/nhands))
print("%.3f%% 0 land hands. %.3f%% 1 land hands. %.3f%% 2 land hands. %.3f%% 3 land hands. %.3f%% 4 land hands. %.3f%% 5 land hands. %.3f%% 6 land hands. %.3f%% 7 land hands." % (total_sample[0]/nhands*100,total_sample[1]/nhands*100,total_sample[2]/nhands*100,total_sample[3]/nhands*100,total_sample[4]/nhands*100,total_sample[5]/nhands*100,total_sample[6]/nhands*100,total_sample[7]/nhands*100))

#Print the stats for a B01 MtGA hand.
bo1_total_sample = collections.Counter(bo1_opening_lands)
print("bo1_total_sample ",bo1_total_sample)
print("Average lands in Bo1 opening hand = %.3f."% (bo1_total_lands/nhands))
print("%.3f%% 0 land hands. %.3f%% 1 land hands. %.3f%% 2 land hands. %.3f%% 3 land hands. %.3f%% 4 land hands. %.3f%% 5 land hands. %.3f%% 6 land hands. %.3f%% 7 land hands." % (bo1_total_sample[0]/nhands*100,bo1_total_sample[1]/nhands*100,bo1_total_sample[2]/nhands*100,bo1_total_sample[3]/nhands*100,bo1_total_sample[4]/nhands*100,bo1_total_sample[5]/nhands*100,bo1_total_sample[6]/nhands*100,bo1_total_sample[7]/nhands*100))

#Plot the histogram for a normal MtG hand and a Bo1 MtGA hand.
fig, ax = plt.subplots(1,2,figsize=(12,12))
binwidth = 1
minbin = 0
maxbin = 7
hopeners = ax[0].hist(opening_lands,bins=np.arange(minbin, maxbin + binwidth, binwidth))
ax[0].set_title("Normal MtG Opening Hand")
ax[0].set_xlabel("Number of Lands in Opening Hand")
ax[0].set_ylabel("Occurrences")
#ax[0].set_xlim(minbin,maxbin)
hb01_openers = ax[1].hist(bo1_opening_lands,bins=np.arange(minbin, maxbin + binwidth, binwidth))
ax[1].set_title("MtGA Best of One Opening Hand")
ax[1].set_xlabel("Number of Lands in Opening Hand")
ax[1].set_ylabel("Occurrences")
#ax[1].set_xlim(minbin,maxbin)
plt.show()

# fig, ax = plt.subplots(figsize=(10,10)) 
# hopeners = ax.hist(opening_lands,bins=7)
# ax.set_xlim(0,7)

# fig, ax = plt.subplots(figsize=(10,10))
# hb01_openers = ax.hist(bo1_opening_lands,bins=7)
# ax.set_xlim(0,7)
# plt.show()
