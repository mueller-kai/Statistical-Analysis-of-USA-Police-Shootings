import pandas as pd
import numpy as np
from collections import Counter
import scipy.stats as stats

#Hypothese 1 
#	HA: Mehr al zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft
#	HO: Weniger als zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft

#read datacolouom date
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv')

#Filter data for unarmed and White race (WUNA)
dfWUNA = df.loc[(df['armed'] == 'unarmed') & (df['race'] == 'W')]

#Filter data for unarmed and Black race (BUNA)
dfBUNA = df.loc[(df['armed'] == 'unarmed') & (df['race'] == 'B')]

#Filter data for unarmed and Hispanic race (HUNA)
dfHUNA = df.loc[(df['armed'] == 'unarmed') & (df['race'] == 'H')]

#Filter data for unarmed and Asian race (HUNA)
dfAUNA = df.loc[(df['armed'] == 'unarmed') & (df['race'] == 'A')]

#Filter data for unarmed and Native race (HUNA)
dfNUNA = df.loc[(df['armed'] == 'unarmed') & (df['race'] == 'N')]

#Accessing the df with only of White Victims 
WV = df.loc[(df['race'] == 'W')]

#Accessing the df with only of Black Victims 
BV = df.loc[(df['race'] == 'B')]

#Accessing the df with only of Hispanic Victims 
HV = df.loc[(df['race'] == 'H')]

#Accessing the df with only of Asian Victims 
AV = df.loc[(df['race'] == 'A')]

#Accessing the df with only of Native Victims 
NV = df.loc[(df['race'] == 'N')]

#Percentage of white unarmed victims
PWUNA = (len(dfWUNA)) / (len(WV))

#Percentage of black unarmed victims
PBUNA = (len(dfBUNA) / len(BV))

#Percentage of HIspanic unarmed victims
PHUNA = (len(dfHUNA) / len(HV))

#Percentage of Asian unarmed victims
PAUNA = (len(dfAUNA) / len(AV))

#Percentage of Native unarmed victims
PNUNA = (len(dfNUNA) / len(NV))

print(PBUNA)

#dfBUNA = dfBUNA['armed']
#dfBUNAstd = dfBUNA.std()

#print(dfBUNA.std())