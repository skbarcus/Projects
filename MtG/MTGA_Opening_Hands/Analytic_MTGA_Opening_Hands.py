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
save_data = 0               #Boolean to decide whether or not to save data. 1 = save data.


normal_opener = []
temp = []
for i in range(minlands,maxlands+1):
    temp.clear()
    land_frac = i/deck_size
    avg_lands = round(land_frac*nopener)
    print("A %d card deck with %d lands has a land fraction of %.3f and will draw %.3f (%f) lands in the opening hand on average." % (deck_size,i,land_frac,land_frac*nopener,avg_lands))
    for j in range(0,nopener+1):
        hpd = ss.hypergeom(deck_size, i, nopener)
        prob = hpd.pmf(j)
        temp.append(prob)
    temp_arr = np.array(temp)
    print(temp_arr)
    normal_opener.append(temp_arr)

normal_opener = np.array(normal_opener)
print(normal_opener[16])
print(normal_opener[17])

#Save the results in numpy arrays if desired.
if save_data == 1:
    print("Data saved to ",data)
    np.save(data + "Analytic_Normal_Openers", normal_openers)
    np.save(data + "Analytic_Bo1_Openers", bo1_openers)

print("The script took %.2f seconds (%.2f minutes or %.2f hours) to run." % (time.time() - start, (time.time() - start)/60.,(time.time() - start)/60./60.)) #Print time to run.
