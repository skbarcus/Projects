from matplotlib import pyplot as plt
import numpy as np
import random
import collections
import time 
import scipy.stats as ss #Has hypergeometric calculator.

start = time.time() #Start a timer.

minlands = 0
maxlands = 40
deck_size = 40
nopener = 7  

data = "/home/skbarcus/Projects/MtG/MTGA_Opening_Hands/Data/" #Directory to store saved data.
save_data = 1               #Boolean to decide whether or not to save data. 1 = save data.


normal_opener = []
bo1_opener = []
temp1 = []
temp2 = []
tot_prob = 0
for i in range(minlands,maxlands+1):
    temp1.clear()
    temp2.clear()
    land_frac = i/deck_size
    avg_lands = round(land_frac*nopener)
    print("A %d card deck with %d lands has a land fraction of %.3f and will draw %.3f (%f) lands in the opening hand on average." % (deck_size,i,land_frac,land_frac*nopener,avg_lands))
    for j in range(0,nopener+1):
        hpd = ss.hypergeom(deck_size, i, nopener)
        prob = hpd.pmf(j)
        temp1.append(prob)
        for k in range(0,nopener+1):
            if abs(land_frac-k/nopener)>abs(land_frac-j/nopener):
                #print("j, k = ",j,"",k)
                bo1_hpd = ss.hypergeom(deck_size, i, nopener)
                bo1_prob = bo1_hpd.pmf(j)*bo1_hpd.pmf(k)
                tot_prob = tot_prob + bo1_prob*2.
        tot_prob = tot_prob + prob*prob
        temp2.append(tot_prob)
        #print("%d lands in opener = %.4f" %(j,tot_prob))
        tot_prob = 0
    temp_arr1 = np.array(temp1)
    temp_arr2 = np.array(temp2)
    #print(temp_arr1)
    normal_opener.append(temp_arr1*100.)
    bo1_opener.append(temp_arr2*100.)

normal_opener = np.array(normal_opener)
#print(normal_opener[0])
#print(normal_opener[1])
bo1_opener = np.array(bo1_opener)
#print(bo1_opener[0])
#print(bo1_opener[1])
normal_opener = [['%.2f' % j for j in i] for i in normal_opener]
bo1_opener = [['%.2f' % j for j in i] for i in bo1_opener]
print("normal_opener = ",normal_opener)
print("bo1_opener = ",bo1_opener)

#Save the results in numpy arrays if desired.
if save_data == 1:
    print("Data saved to ",data)
    np.save(data + "Analytic_Normal_Openers", normal_opener)
    np.save(data + "Analytic_Bo1_Openers", bo1_opener)

print("The script took %.2f seconds (%.2f minutes or %.2f hours) to run." % (time.time() - start, (time.time() - start)/60.,(time.time() - start)/60./60.)) #Print time to run.
