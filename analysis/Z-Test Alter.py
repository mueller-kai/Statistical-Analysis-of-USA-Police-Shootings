import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
#import seaborn as sns

#Angenommen wir haben eine zufällige Auswahl dunkelhäutiger Menschen (n = 30). WIr wollen überprüfen, ob die Daten ein Beweis dafür sind, dass das durchschnittliche Alter
# der getöteten dunkelhäutigen Menschen niedirger ist als der Durchschnitt aller getöteten Menschen die nicht dunkelhäutig waren


#read datacolouom race
df = pd.read_csv (r'C:\Users\mailm\OneDrive\Dokumente\GitHub\statistics-and-machine-learning-project-police-USA\original_data\fatal-police-shootings-data.csv')

##########              Give a data frame with all victims != to Black and drop na values. Gesamtpopulation       #####################

dfpop = df.loc[(df['race'] != 'B')].dropna()
dfpopmean = dfpop['age'].mean() ##give mean age of that Gesamtpopulation

print ("popmean", dfpopmean)

###################################       Getting a sample of 40 Black Victims          ###############################

#drop na values og age coloum and get all Black victims
dfage = df.loc[(df['race'] == 'B')]

#reduce to age coloum
dfage = dfage['age']

#draw a sample of 40
#dfage = dfage.sample(n=50)

#reset index
dfage = dfage.reset_index(drop = True)


###################################       Claculating STD, mean nad z for Sample             ################################
#cal n
n =  len(dfage)
print ("sample size", n)

#calculating mean
dfagemean= dfage.mean()
print ("sampe mean", dfagemean)

#calculating std
dfagestd = dfage.std()
print ("sample std", dfagestd)

#cal se
se = dfagestd / math.sqrt(n)
print ("sample se", se)

#cal z value
z = (dfagemean - dfpopmean) / se
print ("sample z", z)

plt.hist(dfpop['age'])
#dfage.plot()
#plt.show()