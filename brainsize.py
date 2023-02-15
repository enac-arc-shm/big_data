import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

brainFile = 'Data/brainsize.csv'
brainFrame = pd.read_csv(brainFile)

menDf = brainFrame[(brainFrame.Gender == 'Male')]
womenDf = brainFrame[(brainFrame.Gender == 'Female')]


#matplotlib inline
menMeanSmarts = menDf[["PIQ", "FSIQ", "VIQ"]].mean(axis=1)
plt.scatter(menMeanSmarts, menDf["MRI_Count"])
plt.show()

womenMeanSmarts = womenDf[["PIQ", "FSIQ", "VIQ"]].mean(axis=1)
plt.scatter(womenMeanSmarts, womenDf["MRI_Count"])
plt.show()

womenDf.corr(method='pearson')
menDf.corr(method='pearson')
womenNoGenderDf = womenDf.drop('Gender', axis=1)
menNoGenderDf = menDf.drop('Gender', axis=1)

womenNoGenderDf = womenNoGenderDf[womenNoGenderDf.columns].astype(float)
menNoGenderDf = menNoGenderDf[menNoGenderDf.columns].astype(float)

#wcorr = womenNoGenderDf.corr()
#sns.heatmap(wcorr)

mcorr = menNoGenderDf.corr()
sns.heatmap(mcorr)

plt.show()
#sns.heatmap(mcorr)
