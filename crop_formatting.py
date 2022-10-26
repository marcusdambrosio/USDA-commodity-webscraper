import datetime as dt
import sys
import re
import numpy as np
import pandas as pd
import os

def give_daysBack(daysBack):
    '''
    Sets environmental variables
    :param daysBack:
    :return: none
    '''
    os.environ['DAYSBACK'] = str(daysBack)
    os.environ["FILEDATE"] = (dt.datetime.now()-dt.timedelta(daysBack)).strftime('%m-%d-%Y')

def TOMATOES(tomatoes):
    '''
    Formats tomato data from provided dataframe
    :param tomatoes: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    tomatoes = tomatoes[tomatoes['Low Price'].notna()]
    tomatoes = tomatoes[tomatoes['High Price'].notna()]
    for i in tomatoes.index:
        try:
            if ('lb' not in tomatoes.loc[i, 'Package'] and 'kg' not in tomatoes.loc[i, 'Package']) or 'container' in \
                    tomatoes.loc[i, 'Package']:
                tomatoes.drop(i, axis=0, inplace=True)
            elif 'lb' in tomatoes.loc[i, 'Package'] and 'kg' in tomatoes.loc[i, 'Package']:
                tomatoes.loc[i, 'Package'] = tomatoes.loc[i, 'Package'].split('/')[0]
        except:
            tomatoes.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in tomatoes.')
    tomatoes.reset_index(drop=True, inplace=True)
    varieties = tomatoes['Variety']
    organic = tomatoes['Type'].fillna('Nonorganic')
    tomatoes['Type'] = organic
    grades = tomatoes['Grade'].fillna('None')
    low = tomatoes['Low Price']
    high = tomatoes['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    tomatoes = tomatoes.loc[tomatoes['Date'].isin(dates)]

    tomatMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []

    for i, size in enumerate(tomatoes['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            tomatoes.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in tomatoes')
    tomatoes.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    tomatoes['High Price'] = tomatoes['High Price'] / scalers
    tomatoes['Low Price'] = tomatoes['Low Price'] / scalers
    combinations = []
    for row in tomatoes.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = tomatoes[tomatoes['Date'] == date]
        # currDf = currDf[currDf['Package'] == size]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        # currDf['High Price'] = currDf['High Price']
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        tomatMaster = tomatMaster.append({'Date': date,
                                          'Crop': 'Tomatoes',
                                          'Variety': variety,
                                          'Grade': 'N/A',
                                          'High Price': high,
                                          'Low Price': low,
                                          'Average': avg,
                                          'Type': org}, ignore_index=True)

    tomatMaster = tomatMaster[tomatMaster['Variety'].notna()]
    tomatMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/tomatoes.csv', index=False)


def ALMONDS(almonds):
    '''
    Formats almond data from provided dataframe
    :param almonds: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    almonds = almonds[almonds['Low Price'].notna()]
    almonds = almonds[almonds['High Price'].notna()]
    for i in almonds.index:
        try:
            if almonds.loc[i, 'Unit of Sale'] == 'PER LB':
                almonds.loc[i, 'Package'] = '1 lb'
            if '1-lb' in almonds.loc[i, 'Package']:
                almonds.loc[i, 'Package'] = almonds.loc[i, 'Package'].split('1-lb')[0]
        except:
            almonds.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in almonds')
    almonds.reset_index(drop=True, inplace=True)

    varieties = almonds['Variety']
    organic = almonds['Type'].fillna('Nonorganic')
    almonds['Type'] = organic
    grades = almonds['Grade'].fillna('None')
    low = almonds['Low Price']
    high = almonds['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    almonds = almonds.loc[almonds['Date'].isin(dates)]

    almondMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []

    for i, size in enumerate(almonds['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            almonds.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in almonds')
    almonds.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    almonds['High Price'] = almonds['High Price'] / scalers
    almonds['Low Price'] = almonds['Low Price'] / scalers
    combinations = []
    for row in almonds.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = almonds[almonds['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        almondMaster = almondMaster.append({'Date': date,
                                            'Crop': 'almonds',
                                            'Variety': variety,
                                            'Grade': 'N/A',
                                            'High Price': high,
                                            'Low Price': low,
                                            'Average': avg,
                                            'Type': org}, ignore_index=True)

    almondMaster = almondMaster[almondMaster['Variety'].notna()]
    almondMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/almonds.csv', index=False)
    print('ALMONDS COMPLETED \n')


def GRAPES(grapes):
    '''
    Formats grape data from provided dataframe
    :param grapes: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    grapes = grapes[grapes['Low Price'].notna()]
    grapes = grapes[grapes['High Price'].notna()]

    varieties = grapes['Variety']
    organic = grapes['Type'].fillna('Nonorganic')
    grapes['Type'] = organic
    grades = grapes['Grade'].fillna('None')
    low = grapes['Low Price']
    high = grapes['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    grapes = grapes.loc[grapes['Date'].isin(dates)]

    grapeMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []
    grapes.reset_index(drop=True, inplace=True)
    for i, size in enumerate(grapes['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            if type(i) == list:
                i = i[0]
            grapes.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in grapes')
    grapes.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    grapes['High Price'] = grapes['High Price'] / scalers
    grapes['Low Price'] = grapes['Low Price'] / scalers
    combinations = []
    for row in grapes.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = grapes[grapes['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        grapeMaster = grapeMaster.append({'Date': date,
                                          'Crop': 'grapes',
                                          'Variety': variety,
                                          'Grade': 'N/A',
                                          'High Price': high,
                                          'Low Price': low,
                                          'Average': avg,
                                          'Type': org}, ignore_index=True)

    grapeMaster = grapeMaster[grapeMaster['Variety'].notna()]
    grapeMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/grapes.csv', index=False)
    print('grapes COMPLETED \n')


def PISTACHIOS(pistachios):
    '''
    Formats Pistachio data from provided dataframe
    :param pistachios: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    pistachios = pistachios[pistachios['Low Price'].notna()]
    pistachios = pistachios[pistachios['High Price'].notna()]

    for i in pistachios.index:
        try:
            if 'oz' in pistachios.loc[i, 'Package']:
                pistachios.loc[i, 'Package'] = str(24 * 3 / 4)
        except:
            pistachios.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in pistachios')
    pistachios.reset_index(drop=True, inplace=True)

    varieties = pistachios['Variety']
    organic = pistachios['Type'].fillna('Nonorganic')
    pistachios['Type'] = organic
    grades = pistachios['Grade'].fillna('None')
    low = pistachios['Low Price']
    high = pistachios['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    pistachios = pistachios.loc[pistachios['Date'].isin(dates)]

    pistachioMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []

    for i, size in enumerate(pistachios['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            pistachios.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in pistachios')
    pistachios.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    pistachios['High Price'] = pistachios['High Price'] / scalers
    pistachios['Low Price'] = pistachios['Low Price'] / scalers
    combinations = []
    for row in pistachios.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = pistachios[pistachios['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        pistachioMaster = pistachioMaster.append({'Date': date,
                                                  'Crop': 'pistachios',
                                                  'Variety': variety,
                                                  'Grade': 'N/A',
                                                  'High Price': high,
                                                  'Low Price': low,
                                                  'Average': avg,
                                                  'Type': org}, ignore_index=True)

    pistachioMaster = pistachioMaster[pistachioMaster['Variety'].notna()]
    pistachioMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/pistachios.csv', index=False)
    print('pistachios COMPLETED \n')


def STRAWBERRIES(strawberries):
    '''
    Formats strawberry data from provided dataframe
    :param strawberries: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    strawberries = strawberries[strawberries['Low Price'].notna()]
    strawberries = strawberries[strawberries['High Price'].notna()]

    for i in strawberries.index:
        try:
            if type(strawberries.loc[i, 'Variety']) != str:
                strawberries.loc[i, 'Variety'] = 'Base'
            if '8 1-lb' in strawberries.loc[i, 'Package']:
                strawberries.loc[i, 'Package'] = '8 lb'
            elif '4 2-lb' in strawberries.loc[i, 'Package']:
                strawberries.loc[i, 'Package'] = '8 lb'
            elif '2 4-lb' in strawberries.loc[i, 'Package']:
                strawberries.loc[i, 'Package'] = '8 lb'
            elif '6 2-lb' in strawberries.loc[i, 'Package']:
                strawberries.loc[i, 'Package'] = '12 lb'
            elif '4 1-lb' in strawberries.loc[i, 'Package']:
                strawberries.loc[i, 'Package'] = '4 lb'
        except:
            strawberries.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in strawberries')
    strawberries.reset_index(drop=True, inplace=True)

    varieties = strawberries['Variety']
    organic = strawberries['Type'].fillna('Nonorganic')
    strawberries['Type'] = organic
    grades = strawberries['Grade'].fillna('None')
    low = strawberries['Low Price']
    high = strawberries['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    strawberries = strawberries.loc[strawberries['Date'].isin(dates)]

    strawberryMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []

    for i, size in enumerate(strawberries['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            strawberries.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in strawberries')
    strawberries.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    strawberries['High Price'] = strawberries['High Price'] / scalers
    strawberries['Low Price'] = strawberries['Low Price'] / scalers
    combinations = []
    for row in strawberries.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = strawberries[strawberries['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        strawberryMaster = strawberryMaster.append({'Date': date,
                                                    'Crop': 'strawberries',
                                                    'Variety': variety,
                                                    'Grade': 'N/A',
                                                    'High Price': high,
                                                    'Low Price': low,
                                                    'Average': avg,
                                                    'Type': org}, ignore_index=True)

    strawberryMaster = strawberryMaster[strawberryMaster['Variety'].notna()]
    strawberryMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/strawberries.csv', index=False)
    print('strawberries COMPLETED \n')


def ORANGES(oranges):
    '''
    Formats orange data from provided dataframe
    :param oranges: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    oranges = oranges[oranges['Low Price'].notna()]
    oranges = oranges[oranges['High Price'].notna()]

    for i in oranges.index:
        currPack = oranges.loc[i, 'Package']
        try:
            if 'lb' not in currPack and 'kg' not in currPack:
                oranges.drop(i, axis = 0, inplace = True)
                continue
            elif '10 4-lb' in currPack:
                oranges.loc[i, 'Package'] = '40 lb'
            elif '7 4-lb' in currPack:
                oranges.loc[i, 'Package'] = '28 lb'
            elif '9 3-lb' in currPack:
                oranges.loc[i, 'Package'] = '27 lb'
            elif '6 8-lb' in currPack:
                oranges.loc[i, 'Package'] = '48 lb'
            elif '15-16 kg' in currPack:
                oranges.loc[i, 'Package'] = '15 kg'
        except Exception as e:
            oranges.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in oranges\n'
                  f'{e}')
    oranges.reset_index(drop=True, inplace=True)

    varieties = oranges['Variety']
    organic = oranges['Type'].fillna('Nonorganic')
    oranges['Type'] = organic
    grades = oranges['Grade'].fillna('None')
    low = oranges['Low Price']
    high = oranges['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    oranges = oranges.loc[oranges['Date'].isin(dates)]

    orangeMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []
    oranges.reset_index(drop=True, inplace=True)
    for i, size in enumerate(oranges['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except Exception as e:
            if type(i) == list:
                i = i[0]
            oranges.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in oranges\n'
                  f'{e}')
    oranges.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    oranges['High Price'] = oranges['High Price'] / scalers
    oranges['Low Price'] = oranges['Low Price'] / scalers
    combinations = []
    for row in oranges.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = oranges[oranges['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        orangeMaster = orangeMaster.append({'Date': date,
                                            'Crop': 'oranges',
                                            'Variety': variety,
                                            'Grade': 'N/A',
                                            'High Price': high,
                                            'Low Price': low,
                                            'Average': avg,
                                            'Type': org}, ignore_index=True)

    orangeMaster = orangeMaster[orangeMaster['Variety'].notna()]
    orangeMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/oranges.csv', index=False)
    print('oranges COMPLETED \n')


def CHERRIES(cherries):
    '''
    Formats cherries data from provided dataframe
    :param cherries: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    cherries = cherries[cherries['Low Price'].notna()]
    cherries = cherries[cherries['High Price'].notna()]
    for i in cherries.index:
        currPack = cherries.loc[i, 'Package']
        try:
            if 'lb' not in currPack and 'kg' not in currPack and 'oz' not in currPack:
                cherries.drop(i, axis=0, inplace=True)
                continue
            elif '8 2.25-lb' in currPack:
                cherries.loc[i, 'Package'] = '18 lb'
            elif '8 3-lb' in currPack:
                cherries.loc[i, 'Package'] = '24 lb'
            elif '18 16-oz' in currPack:
                cherries.loc[i, 'Package'] = '18 lb'
        except:
            cherries.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in cherries')
    cherries.reset_index(drop=True, inplace=True)

    varieties = cherries['Variety']
    organic = cherries['Type'].fillna('Nonorganic')
    cherries['Type'] = organic
    grades = cherries['Grade'].fillna('None')
    low = cherries['Low Price']
    high = cherries['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    cherries = cherries.loc[cherries['Date'].isin(dates)]

    cherryMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []
    cherries.reset_index(drop=True, inplace=True)
    for i, size in enumerate(cherries['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            if type(i) == list:
                i = i[0]
            cherries.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in cherries')
    cherries.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    cherries['High Price'] = cherries['High Price'] / scalers
    cherries['Low Price'] = cherries['Low Price'] / scalers
    combinations = []
    for row in cherries.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = cherries[cherries['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        cherryMaster = cherryMaster.append({'Date': date,
                                            'Crop': 'cherries',
                                            'Variety': variety,
                                            'Grade': 'N/A',
                                            'High Price': high,
                                            'Low Price': low,
                                            'Average': avg,
                                            'Type': org}, ignore_index=True)

    cherryMaster = cherryMaster[cherryMaster['Variety'].notna()]
    cherryMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/cherries.csv', index=False)
    print('cherries COMPLETED \n')


def LETTUCE(lettuce):
    '''
    Formats lettuce data from provided dataframe
    :param lettuce: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    lettuce = lettuce[lettuce['Low Price'].notna()]
    lettuce = lettuce[lettuce['High Price'].notna()]

    for i in lettuce.index:
        currPack = lettuce.loc[i, 'Package']
        try:
            if 'lb' not in currPack and 'kg' not in currPack and 'oz' not in currPack:
                lettuce.drop(i, axis=0, inplace=True)
                continue
            elif '12 4-oz' in currPack:
                lettuce.loc[i, 'Package'] = '3 lb'
            elif '12 22-oz' in currPack:
                lettuce.loc[i, 'Package'] = '16.5 lb'
            elif '12 24.2' in currPack:
                lettuce.loc[i, 'Package'] = '18.15 lb'
        except:
            lettuce.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in lettuce')
    lettuce.reset_index(drop=True, inplace=True)

    varieties = lettuce['Variety']
    organic = lettuce['Type'].fillna('Nonorganic')
    lettuce['Type'] = organic
    grades = lettuce['Grade'].fillna('None')
    low = lettuce['Low Price']
    high = lettuce['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    lettuce = lettuce.loc[lettuce['Date'].isin(dates)]

    lettuceMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []
    lettuce.reset_index(drop=True, inplace=True)
    for i, size in enumerate(lettuce['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            if type(i) == list:
                i = i[0]
            lettuce.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in lettuce')
    lettuce.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    lettuce['High Price'] = lettuce['High Price'] / scalers
    lettuce['Low Price'] = lettuce['Low Price'] / scalers
    combinations = []
    for row in lettuce.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = lettuce[lettuce['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        lettuceMaster = lettuceMaster.append({'Date': date,
                                              'Crop': 'lettuce',
                                              'Variety': variety,
                                              'Grade': 'N/A',
                                              'High Price': high,
                                              'Low Price': low,
                                              'Average': avg,
                                              'Type': org}, ignore_index=True)

    lettuceMaster = lettuceMaster[lettuceMaster['Variety'].notna()]
    lettuceMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/lettuce.csv', index=False)
    print('lettuce COMPLETED \n')


def BLUEBERRIES(blueberries):
    '''
    Formats blueberry data from provided dataframe
    :param blueberries: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    blueberries = blueberries[blueberries['Low Price'].notna()]
    blueberries = blueberries[blueberries['High Price'].notna()]
    for i in blueberries.index:
        currPack = blueberries.loc[i, 'Package']
        try:
            if 'lb' not in currPack and 'kg' not in currPack and 'oz' not in currPack:
                blueberries.drop(i, axis=0, inplace=True)
                continue
            elif '12 1-pt' in currPack:
                blueberries.loc[i, 'Package'] = '9 lb'
            elif '12 6-oz' in currPack:
                blueberries.loc[i, 'Package'] = '4.5 lb'
            elif '12 11-oz' in currPack:
                blueberries.loc[i, 'Package'] = '8.25 lb'
            elif '12 4.4-oz' in currPack:
                blueberries.loc[i, 'Package'] = '3.3 lb'
            elif '12 8-oz' in currPack:
                blueberries.loc[i, 'Package'] = '6 lb'
            elif '12 18-oz' in currPack:
                blueberries.loc[i, 'Package'] = '13.5 lb'
            elif '8 18-oz' in currPack:
                blueberries.loc[i, 'Package'] = '9 lb'
            elif '12 250-gm' in currPack:
                blueberries.loc[i, 'Package'] = '3 kg'
        except:
            blueberries.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in blueberries')
    blueberries.reset_index(drop=True, inplace=True)
    organic = blueberries['Type'].fillna('Nonorganic')
    blueberries['Type'] = organic
    grades = blueberries['Grade'].fillna('None')
    low = blueberries['Low Price']
    high = blueberries['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    blueberries = blueberries.loc[blueberries['Date'].isin(dates)]

    blueberryMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []
    blueberries.reset_index(drop=True, inplace=True)
    for i, size in enumerate(blueberries['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            if type(i) == list:
                i = i[0]
            blueberries.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in blueberries')
    blueberries.reset_index(drop=True, inplace=True)
    scalers = np.array(scalers)
    blueberries['High Price'] = blueberries['High Price'] / scalers
    blueberries['Low Price'] = blueberries['Low Price'] / scalers
    combinations = []
    for row in blueberries.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = blueberries[blueberries['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        blueberryMaster = blueberryMaster.append({'Date': date,
                                                  'Crop': 'blueberries',
                                                  'Variety': 'N/A',
                                                  'Grade': 'N/A',
                                                  'High Price': high,
                                                  'Low Price': low,
                                                  'Average': avg,
                                                  'Type': org}, ignore_index=True)


    blueberryMaster = blueberryMaster[blueberryMaster['Variety'].notna()]
    blueberryMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/blueberries.csv', index=False)
    print('blueberries COMPLETED \n')


def APRICOTS(apricots):
    '''
    Formats apricot data from provided dataframe
    :param apricots: pd.DataFrame()
    :return: saves as newly formatted csv file
    '''
    apricots = apricots[apricots['Low Price'].notna()]
    apricots = apricots[apricots['High Price'].notna()]

    for i in apricots.index:
        currPack = apricots.loc[i, 'Package']
        try:
            if 'lb' not in currPack and 'kg' not in currPack and 'oz' not in currPack:
                apricots.drop(i, axis=0, inplace=True)
                continue
        except:
            apricots.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in apricots')
    apricots.reset_index(drop=True, inplace=True)

    varieties = apricots['Variety']
    organic = apricots['Type'].fillna('Nonorganic')
    apricots['Type'] = organic
    grades = apricots['Grade'].fillna('None')
    low = apricots['Low Price']
    high = apricots['High Price']
    dates = [(dt.datetime.today() - dt.timedelta(days=int(os.environ['DAYSBACK']))) + dt.timedelta(days=d) for d in range(int(os.environ['DAYSBACK']) + 1)]
    dates = [d.strftime('%m/%d/%Y') for d in dates]
    apricots = apricots.loc[apricots['Date'].isin(dates)]

    apricotMaster = pd.DataFrame(
        columns=['Date', 'Crop', 'Variety', 'Grade', 'High Price', 'Low Price', 'Average', 'Type'])
    scalers = []
    apricots.reset_index(drop=True, inplace=True)
    for i, size in enumerate(apricots['Package']):
        try:
            scalers.append(
                float(re.sub("[^0-9.]", "", size)) if 'lb' in size else float(re.sub("[^0-9.]", "", size)) * 2.20462)
        except:
            if type(i) == list:
                i = i[0]
            apricots.drop(i, axis=0, inplace=True)
            print(f'line {i} failed in apricots')
    apricots.reset_index(drop=True, inplace=True)

    scalers = np.array(scalers)
    apricots['High Price'] = apricots['High Price'] / scalers
    apricots['Low Price'] = apricots['Low Price'] / scalers
    combinations = []
    for row in apricots.iterrows():
        i, row = row
        combinations.append([row['Date'], row['Type'], row['Variety']])
    uniqueCombos = []
    for c in combinations:
        if c not in uniqueCombos:
            uniqueCombos.append(c)

    for combo in uniqueCombos:
        date, org, variety = combo
        currDf = apricots[apricots['Date'] == date]
        currDf = currDf[currDf['Type'] == org]
        currDf = currDf[currDf['Variety'] == variety]
        high = currDf['High Price'].max()
        low = currDf['Low Price'].min()
        avg = np.mean((currDf['High Price'] + currDf['Low Price']) / 2)
        apricotMaster = apricotMaster.append({'Date': date,
                                              'Crop': 'apricots',
                                              'Variety': variety,
                                              'Grade': 'N/A',
                                              'High Price': high,
                                              'Low Price': low,
                                              'Average': avg,
                                              'Type': org}, ignore_index=True)

    apricotMaster = apricotMaster[apricotMaster['Variety'].notna()]
    apricotMaster.to_csv(f'downloads/{os.environ["FILEDATE"].replace("/", "-")}/apricots.csv', index=False)
    print('apricots COMPLETED \n')