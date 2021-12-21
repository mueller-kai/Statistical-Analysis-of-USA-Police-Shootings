import pandas as pd
import numpy as np
from collections import Counter
import scipy.stats as stats

#Hypothese 1 
#	HA: Mehr al zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft
#	HO: Weniger als zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft

#read datacolouom date
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv')

#Filter data for only White and BLack
df = df.loc[(df['race'] == 'W') | (df['race'] == 'N')]

#Filter for armed victims
ArmedM = np.array(pd.crosstab(df ['armed'] == 'unarmed', df ['race']))

#perform Chisquare Test
X2 = stats.chi2_contingency(ArmedM, correction=False)[0]
n = np.sum(ArmedM)
minDim = min(ArmedM.shape)-1

#printing Results
print(ArmedM)
print(X2)

V = np.sqrt((X2/n) / minDim)
print (V)
