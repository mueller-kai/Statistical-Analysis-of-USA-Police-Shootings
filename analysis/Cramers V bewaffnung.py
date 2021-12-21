import pandas as pd
import numpy as np
from collections import Counter
import scipy.stats as stats
import researchpy

#read datacolouom date
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv')
df = df.replace(to_replace =["gun", "car", "toy weapon", "nail gun", "screw driver", "undetermined", "screwdriver", "hammer"], value ="armed") 

#filter for armed unarmed
df = df.loc[(df['armed'] == 'unarmed') | (df['armed'] == "armed")]

#Filter data for only 2 drifferent Races
df = df.loc[(df['race'] == 'W') | (df['race'] == 'N')]

#creating crosstable
crosstab, res = researchpy.crosstab(df['armed'], df['race'], test='chi-square')

print (crosstab)
print (res)
