from matplotlib import pyplot as plt
import numpy as np
import random
import collections
import time
import scipy.stats as ss #Has hypergeometric calculator.

start = time.time() #Start a timer.

minlands = 14
maxlands = 20
deck_size = 40
nopener = 7

Normal_Openers = np.load("/home/skbarcus/Projects/MtG/MTGA_Opening_Hands/Data/Analytic_Normal_Openers.npy")
Bo1_Openers = np.load("/home/skbarcus/Projects/MtG/MTGA_Opening_Hands/Data/Analytic_Bo1_Openers.npy")

#Create smaller array for the table of results. 
norm_results = []
bo1_results = []
temp1 = []
temp2 = []
for i in range(minlands,maxlands+1):
    norm_results.append(Normal_Openers[i])
    norm_results.append(Bo1_Openers[i])

#print(Normal_Openers[16])
#print(Normal_Openers[17])
#print(Bo1_Openers[16])
#print(Bo1_Openers[17])
norm_results = np.array(norm_results)
#Ensure just two decimal places.
#norm_results = [['%.2f' % j for j in i] for i in norm_results]
#print(norm_results)

###
#Main results table.
###
#Set column labels.
cols = ("% 0 Lands","% 1 Lands","% 2 Lands","% 3 Lands","% 4 Lands","% 5 Lands","% 6 Lands","% 7 Lands")

#Set row labels.
rows = []
for i in range(minlands,maxlands+1):
    rows.append("%d Lands" % i)
    rows.append("%d Lands Bo1" % i)

#Set column widths.
widths = []
for i in range(0,len(cols)):
    widths.append(0.045)

#Add background colors for the cells.
colors = []
for i in range(0,len(rows)):
    if i%2==0:
        colors_temp1 = []
        for j in range(0,len(cols)):
            colors_temp1.append("cyan")
        #colors_temp1 = np.array(colors_temp1)
        colors.append(colors_temp1)
    else:
        colors_temp2 = []
        for j in range(0,len(cols)):
            colors_temp2.append("orange")
        #colors_temp2 = np.array(colors_temp2)
        colors.append(colors_temp2)
#print(colors)
col_colors = []
row_colors = []
for i in range(0,len(rows)):
    if i%2==0:
        row_colors.append("darkcyan")
    else:
        row_colors.append("darkorange")
for i in range(0,len(cols)):
    col_colors.append("silver")


fig, ax = plt.subplots(figsize=(16,12))
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
table = plt.table(cellText=norm_results,rowLabels=rows,colLabels=cols,loc='center',colWidths=widths,cellColours=colors,rowColours=row_colors,colColours=col_colors,cellLoc="center")
#table.auto_set_font_size(False)
#table.set_fontsize(24)
table.scale(2.2, 2.2)
plt.show()
###
#End main results table.
###

###
#Combined 2-4 lands results table.
###

#Make array with the combined probabilities data.
combined_norm_results = []
combined_bo1_results = []
temp1 = []
temp2 = []
for i in range(0,(maxlands+1-minlands)*2):
    temp1.clear()
    temp2.clear()
    if i%2 == 0:
        temp1.append(float(norm_results[i][2])+float(norm_results[i][3]))
        temp1.append(float(norm_results[i][3])+float(norm_results[i][4]))
        temp1.append(float(norm_results[i][2])+float(norm_results[i][3])+float(norm_results[i][4]))
        temp1_arr = np.array(temp1)
        combined_norm_results.append(temp1_arr)
    else:
        temp2.append(float(norm_results[i][2])+float(norm_results[i][3]))
        temp2.append(float(norm_results[i][3])+float(norm_results[i][4]))
        temp2.append(float(norm_results[i][2])+float(norm_results[i][3])+float(norm_results[i][4]))
        temp2_arr = np.array(temp2)
        combined_norm_results.append(temp2_arr)

combined_norm_results = np.array(combined_norm_results)
combined_norm_results = [['%.2f' % j for j in i] for i in combined_norm_results]
print("combined_norm_results = ",combined_norm_results)
#Set column labels.
combined_cols = ("% 2-3 Lands","% 3-4 Lands","% 2-4 Lands")

#Set row labels.
combined_rows = []
for i in range(minlands,maxlands+1):
    combined_rows.append("%d Lands" % i)
    combined_rows.append("%d Lands Bo1" % i)

#Set column widths.
combined_widths = []
for i in range(0,len(combined_cols)):
    combined_widths.append(0.045)

#Add background colors for the cells.
combined_colors = []
for i in range(0,len(combined_rows)):
    if i%2==0:
        colors_temp1 = []
        for j in range(0,len(combined_cols)):
            colors_temp1.append("cyan")
        combined_colors.append(colors_temp1)
    else:
        colors_temp2 = []
        for j in range(0,len(combined_cols)):
            colors_temp2.append("orange")
        combined_colors.append(colors_temp2)
print(combined_colors)

combined_col_colors = []
combined_row_colors = []
for i in range(0,len(combined_rows)):
    if i%2==0:
        combined_row_colors.append("darkcyan")
    else:
        combined_row_colors.append("darkorange")
for i in range(0,len(combined_cols)):
    combined_col_colors.append("silver")

fig, ax = plt.subplots(figsize=(16,12))
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
combined_table = plt.table(cellText=combined_norm_results,rowLabels=combined_rows,colLabels=combined_cols,loc='center',colWidths=combined_widths,cellColours=combined_colors,rowColours=combined_row_colors,colColours=combined_col_colors,cellLoc="center")
#table.auto_set_font_size(False)
#table.set_fontsize(24)
combined_table.scale(2.2, 2.2)
plt.show()
###
#End combined results table.
###

###
#40 card deck with 17 lands probabilities of having x lands on turn x with y lands in opener. 
###
curve_probs = []
temp = []
p = 0
for i in range(1,4):
    temp.clear()
    for j in range(2,7):
        hpd = ss.hypergeom(deck_size-nopener, 17-i, j-1)
        for k in range(0,i):
            p = p + hpd.pmf(j-i+k)
            print("i, j, k, p = ",i,"",j,"",k,"",p)
            print("j-i+k = ",j-i+k,"hpd.pmf(j-i+k)",hpd.pmf(j-i+k))
        if i>=j:
            temp.append(1.)
        else:
            temp.append(p)
        p = 0
    temp_arr = np.array(temp)
    curve_probs.append(temp_arr)

curve_probs = np.array(curve_probs)
print(curve_probs)

M = 33  # Total number of cards after drawing opening 7.
n = 14  # Number of lands left in deck.
N = 4   # Number of draws to find a land.
k = 4   # Number of lands we want to draw.
import scipy.stats as ss
hpd = ss.hypergeom(M, n, N)
p = hpd.pmf(k)+hpd.pmf(4)
print("Probability of drawing one land = ",p)
"""
M_start = 40  # Total number of cards after drawing opening 7.
n_start = 17  # Number of lands left in deck.
N_start = 7   # Number of draws to find a land.
k_start = 7   # Number of lands we want to draw.
hpd_start = ss.hypergeom(M_start, n_start, N_start)
p_start = hpd_start.pmf(k_start)
print("Probability of drawing 3 land in opening hand = ",p_start)
"""
print("The script took %.2f seconds (%.2f minutes or %.2f hours) to run." % (time.time() - start, (time.time() - start)/60.,(time.time() - start)/60./60.)) #Print time to run.
