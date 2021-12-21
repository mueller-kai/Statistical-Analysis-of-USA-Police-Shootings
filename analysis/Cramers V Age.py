import pandas as pd
import numpy as np
from collections import Counter
import scipy.stats as stats
import researchpy

#read datacolouom date
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv')
df = df.replace(to_replace =["H", "W", "O", "A", "N"], value ="!B").dropna()

#creating crosstab for chisquare
crosstab, res = researchpy.crosstab(df['age'], df['race'], test='chi-square')

print (crosstab)
print (res)
