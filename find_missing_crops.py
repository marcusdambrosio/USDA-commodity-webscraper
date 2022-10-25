import pandas as pd
import sys,os,time
import dropdown_elements

master = pd.read_excel('6-22-2021_allcrops.xlsx')
crops = master['Commodity Name'].unique()
print(crops)
for crop in dropdown_elements.crops:
    if crop not in crops:
        print(crop)