from matplotlib import pyplot as plt
import numpy as np
import random
import collections
import time 

start = time.time() #Start a timer.

minlands = 14
maxlands = 20

Normal_Openers = np.load("/home/skbarcus/Projects/MtG/MTGA_Opening_Hands/Data/Normal_Openers.npy")
Bo1_Openers = np.load("/home/skbarcus/Projects/MtG/MTGA_Opening_Hands/Data/Bo1_Openers.npy")

#Create smaller array for the table of results. 
norm_results = []
bo1_results = []
temp1 = []
temp2 = []
for i in range(minlands,maxlands+1):
    temp1.clear()
    temp2.clear()
    for j in range(0,len(Normal_Openers[1])):
        if(j>1 and (j % 2 == 1)):
            temp1.append(Normal_Openers[i][j])
            temp2.append(Bo1_Openers[i][j])
    temp1_arr = np.array(temp1)
    temp2_arr = np.array(temp2)
    print(temp2_arr)
    norm_results.append(temp1_arr)
    norm_results.append(temp2_arr)

#print(Normal_Openers[16])
#print(Normal_Openers[17])
print(Bo1_Openers[16])
print(Bo1_Openers[17])
norm_results = np.array(norm_results)
norm_results = [['%.2f' % j for j in i] for i in norm_results]
print(norm_results)

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

print("The script took %.2f seconds (%.2f minutes or %.2f hours) to run." % (time.time() - start, (time.time() - start)/60.,(time.time() - start)/60./60.)) #Print time to run.
