import pandas as pd
import numpy as np
import os, sys, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import dropdown_elements
import datetime as dt
from openpyxl import load_workbook
import re
import pyexcel
import math



def main():
    URL = 'https://www.merlofarminggroup.com/markets'
    driver = webdriver.Chrome()
    driver.get(URL)

    morePage = True
    tableName = 'view view-rice-price-table-2 view-id-rice_price_table_2 view-display-id-block_2 pricing-table view-dom-id-e95ce215a3b4d7a7a4e9615af9ce6b37 jquery-once-1-processed refresh-processed'
    xpath = '/html/body/div[2]/div[3]/div/div/div/section/div[1]'
    master = pd.DataFrame()

    def process_data(master, newData):
        lines = newData.split('\n')
        lines = lines[2:-3]
        for line in lines:
            splitInd = line.find('/') - 2
            variety=line[:splitInd].strip()
            otherData = [c.strip() for c in line[splitInd:].strip().split(' ')]
            master = master.append({'variety':variety,
                                    'date':otherData[0],
                                    'currentPrice':otherData[1],
                                    'previousPrice':otherData[2],
                                    'change':otherData[3]/100}, ignore_index = True)
            return master

    while morePage:
        tableData = driver.find_element_by_xpath(xpath).text
        master = process_data(master, tableData)
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/section/div[1]/div[13]/ul/li[3]/a').click()
            time.sleep(1)
        except:
            print('shit failed')
            morePage = False

    master.to_csv('merlo_data.csv', index = False)
    print('death')



if __name__ == '__main__':
    main()

