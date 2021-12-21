import pandas as pd
import numpy as np

#Hypothese 1 
#	HA: Mehr al zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft
#	HO: Weniger als zwei drittel der von der Polizei in Amerika getöteten Menschen sind afroamerikanischer Herkunft

#
#read datacolouom race
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv')

#creates a series with all relativ(percentage) Values for all races in a descending manner
df = df['age'].mean()

print(df)
