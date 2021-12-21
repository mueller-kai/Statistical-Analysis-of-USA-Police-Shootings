import pandas as pd
import numpy as np

#Hypothese 1 
#	HA: Mehr al zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft
#	HO: Weniger als zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft

#
#read datacolouom race
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv', usecols=['race'])


#creates a series with all relativ(percentage) Values for all races in a descending manner
seriesrace = df['race'].value_counts(normalize = False)

#Assigning series values to objects that can be added
#Note: accessing values vie [:1] or [1:] was not possibel because series values were not hashable
whites = seriesrace[0]
blacks = seriesrace[1] 
hispanic = seriesrace[2]
asian = seriesrace[3]
native_amer = seriesrace[4]
other = seriesrace[5]

sum_nonBlackorHispanic = ( 1 - (blacks + hispanic))

print (seriesrace)

####Experimental######
#converting series to numpy series as pandas series is not hashalbe and therefore can not be accessed via [] index
#seriesrace.to_numpy
#print(seriesrace.sum([0], [1]))