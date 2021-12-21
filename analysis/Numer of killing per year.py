import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib as mpl

#Hypothese 1 
#	HA: Mehr al zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft
#	HO: Weniger als zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft

#read datacolouom date
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv', usecols=['date'])

#converting df to series because datetimeindex funcion needs series as input
seriesdate = (df['date'])

#acessing only year. seriesdate = to a List of the years
seriesdate = pd.DatetimeIndex(seriesdate).month

#using Counter 
cs = seriesdate.Counter()

print(cs)
