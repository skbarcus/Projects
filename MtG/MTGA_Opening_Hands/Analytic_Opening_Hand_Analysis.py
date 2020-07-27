from matplotlib import pyplot as plt
import numpy as np
import random
import collections
import time
import scipy.stats as ss #Has hypergeometric calculator. 
import seaborn as sns #for nicer graphics
#sns.set(color_codes=True)

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
curve_probs_temp = []
temp1 = []
temp2 = []
p_play = 0
p_draw = 0
for z in range(minlands,maxlands+1):#(minlands+1,maxlands)
    curve_probs_temp.clear()
    for i in range(1,4):
        temp1.clear()
        temp2.clear()
        for j in range(2,7):
            hpd_play = ss.hypergeom(deck_size-nopener, z-i, j-1)
            hpd_draw = ss.hypergeom(deck_size-nopener, z-i, j)
            for k in range(0,i):
                p_play = p_play + hpd_play.pmf(j-i+k)
                #p_draw = p_draw + hpd_draw.pmf(j-i+k)
                #print("i, j, k, p_play = ",i,"",j,"",k,"",p_play)
                #print("ss.hypergeom(%d,%d,%d) , hpd_play.pmf(%d) = %f" % (deck_size-nopener, z-i, j-1,j-i+k,hpd_play.pmf(j-i+k)))
            for k in range(0,i+1):
                p_draw = p_draw + hpd_draw.pmf(j-i+k)
                #print("i, j, k, p_draw = ",i,"",j,"",k,"",p_draw)
                #print("ss.hypergeom(%d,%d,%d) , hpd_draw.pmf(%d) = %f" % (deck_size-nopener, z-i, j,j-i+k,hpd_draw.pmf(j-i+k)))
            if i>=j:
                temp1.append(1.)
                temp2.append(1.)
            else:
                temp1.append(p_play)
                temp2.append(p_draw)
            p_play = 0
            p_draw = 0
            #print("********")
        temp_arr1 = np.array(temp1)
        temp_arr2 = np.array(temp2)
        curve_probs_temp.append(temp_arr1)
        curve_probs_temp.append(temp_arr2)
    curve_probs_temp_arr = np.array(curve_probs_temp)
    curve_probs.append(curve_probs_temp_arr)

curve_probs = np.array(curve_probs)
#Convert to percentages.
curve_probs = curve_probs*100.
#Store just two decimals so it's nice to read.
#curve_probs = [['%.2f' % j for j in i] for i in curve_probs]
curve_probs = [[['%.2f' % k for k in j] for j in i] for i in curve_probs]
print(curve_probs)

#Set column labels.
curve_cols = ("% 2 Lands on 2","% 3 Lands on 3","% 4 Lands on 4","% 5 Lands on 5","% 6 Lands on 6")

#Set row labels.
curve_rows = []
for i in range(1,4):
    curve_rows.append("%d Lands on Play" % i)
    curve_rows.append("%d Lands on Draw" % i)

#Set column widths.
curve_widths = []
for i in range(0,len(curve_cols)):
    curve_widths.append(0.045)

#Add background colors for the cells.
curve_colors = []
for i in range(0,len(curve_rows)):
    if i%2==0:
        curve_temp1 = []
        for j in range(0,len(curve_cols)):
            curve_temp1.append("cyan")
        curve_colors.append(curve_temp1)
    else:
        curve_temp2 = []
        for j in range(0,len(curve_cols)):
            curve_temp2.append("orange")
        curve_colors.append(curve_temp2)
print(curve_colors)

curve_col_colors = []
curve_row_colors = []
for i in range(0,len(curve_rows)):
    if i%2==0:
        curve_row_colors.append("darkcyan")
    else:
        curve_row_colors.append("darkorange")
for i in range(0,len(curve_cols)):
    curve_col_colors.append("silver")

for i in range(0,7):
    fig, ax = plt.subplots(figsize=(16,12))
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    curve_table = plt.table(cellText=curve_probs[i],rowLabels=curve_rows,colLabels=curve_cols,loc='center',colWidths=curve_widths,cellColours=curve_colors,rowColours=curve_row_colors,colColours=curve_col_colors,cellLoc="center")
    #table.auto_set_font_size(False)
    #table.set_fontsize(24)
    curve_table.scale(2.2, 2.2)
    plt.show()

M = 33  # Total number of cards after drawing opening 7.
n = 16  # Number of lands left in deck.
N = 2   # Number of draws to find a land.
k = 1   # Number of lands we want to draw.
import scipy.stats as ss
hpd = ss.hypergeom(M, n, N)

p = hpd.pmf(2)+hpd.pmf(3)+hpd.pmf(4)
print(hpd.pmf(2))
print(hpd.pmf(3))
print(hpd.pmf(4))
print("Probability of drawing one land = ",hpd.pmf(k)+hpd.pmf(k+1))
"""
M_start = 40  # Total number of cards after drawing opening 7.
n_start = 17  # Number of lands left in deck.
N_start = 7   # Number of draws to find a land.
k_start = 7   # Number of lands we want to draw.
hpd_start = ss.hypergeom(M_start, n_start, N_start)
p_start = hpd_start.pmf(k_start)
print("Probability of drawing 3 land in opening hand = ",p_start)
"""

#Create histograms of average lands in opening hand for 14-20 lands in a 40 card deck.
binwidth = 1
minbin = 0
maxbin = 7
nhands = 1e4
transparency = 0.5

#Create results for histograms.
histo_results = norm_results
histo_results = [[float(j) for j in i] for i in histo_results]
histo_results = np.array(histo_results)
#Draw a sample of nhands with the proper probability distributions.
histo_results = histo_results*0.01*nhands

xaxis = []
for i in range(0,len(histo_results[0])):
    xaxis.append(i)

labels = []
for i in range(minlands,maxlands+1):
    labels.append(i)

kwargs = kwargs = dict(bins=np.arange(minbin, maxbin + binwidth, binwidth),alpha=transparency,density=True,edgecolor="black",histtype='stepfilled')#,label=labels)

#Plot histo for normal and bo1 17 land hands.
fig, ax = plt.subplots(figsize=(10,10))
hist1 = ax.hist(xaxis,weights=histo_results[6],**kwargs,label="17 Land Deck Normal Draw")
hist2 = ax.hist(xaxis,weights=histo_results[7],**kwargs,label="17 Land Deck Bo1 Draw")
plt.xlabel("Number of Lands in Starting Hand")
plt.ylabel("Rate of Occurrence")
plt.title("Distribution of Lands in Opening Hand: Normal Draw vs. MTGA Bo1 Draw")
ax.legend(prop={'size': 10})
plt.show()

kde_plots = []
temp = []
for i in range(0,histo_results.shape[0]):
    temp.clear()
    for j in range(0,histo_results.shape[1]):
        for k in range(0,int(histo_results[i][j])):
            temp.append(j)
    temp_arr = np.array(temp)
    kde_plots.append(temp_arr)
#print(kde_plots)        

dist = collections.Counter(kde_plots[6])
print(dist)

fig, ax = plt.subplots(figsize=(10,10))
#hist1 = ax.hist(kde_plots[6],**kwargs)
for i in range(0,histo_results.shape[0]):
    if i%2==0:
        sns.kdeplot(kde_plots[i],ax=ax,linewidth=2.0,gridsize=200,bw=.42,legend=True,label="%d Land Deck" % (minlands+i/2))#,shade=True)#,bw=.42)
#ax.legend(labels,prop={'size': 10})#Legend is the shaded colors if kdeplot is shaded.
plt.xlabel("Number of Lands in Starting Hand")
plt.ylabel("Rate of Occurrence")
plt.title("Distribution of Lands in a Normal Opening Hand Based on Number of Lands in Deck")
plt.show()

fig, ax = plt.subplots(figsize=(10,10))
#hist1 = ax.hist(kde_plots[6],**kwargs)
for i in range(0,histo_results.shape[0]):
    if i%2==1:
        sns.kdeplot(kde_plots[i],ax=ax,linewidth=2.0,gridsize=200,bw=.62,legend=True,label="%d Land Deck" % (minlands+i/2))#,shade=True)#,bw=.42)
#ax.legend(labels,prop={'size': 10})#Legend is the shaded colors if kdeplot is shaded.
#ax.plot(linewidth=2.0)
plt.xlabel("Number of Lands in Starting Hand")
plt.ylabel("Rate of Occurrence")
plt.title("Distribution of Lands in an MTGA Bo1 Opening Hand Based on Number of Lands in Deck")
plt.show()

"""
histos = []
#histos = [None] * 10
#plt.style.use('seaborn-white')
#Plot histo for all normal hands 14-20.
fig, ax = plt.subplots(figsize=(10,10))
for i in range(0+2,histo_results.shape[0]-2):
    if i%2==0:
        #histos.append([])
        histos.append(ax.hist(xaxis,weights=histo_results[i],**kwargs))
        #sns.kdeplot(xaxis)
ax.legend(labels,prop={'size': 10})
plt.show()
"""

print("The script took %.2f seconds (%.2f minutes or %.2f hours) to run." % (time.time() - start, (time.time() - start)/60.,(time.time() - start)/60./60.)) #Print time to run.
