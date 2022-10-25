import pandas as pd
import matplotlib.pyplot as plt
import sys, os


almonds = pd.read_csv('downloads/08-14-2011/almonds.csv')
almonds = almonds.iloc[-365:, :]
high = almonds['High Price']
low = almonds['Low Price']

avg = almonds['Average']

labels = ['high' , 'low', 'avg']
for i,dtype in enumerate([high, low, avg]):
    plt.plot(almonds.Date , dtype, label = labels[i])

plt.legend()

plt.show()