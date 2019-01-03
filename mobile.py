from splinter import Browser
import time

from bs4 import BeautifulSoup
import urllib.request

import pickle
import csv

meseci_dict = {'януари':'1',
                'февруари':'2',
                'март':'3',
                'април':'4',
                'май':'5',
                'юни':'6',
                'юли':'7',
                'август':'8',
                'септември':'9',
                'октомври':'10',
                'ноември':'11',
                'декември':'12'}


sleep_time = 1
#Sortirane spored (Цена, Дата на производство, Най-новите обяви от посл. 2 дни)
sortirane = 'Цена'

searches = []
#Region i grad (empty to skip)
#opcii = ['4x4', 'Парктроник', 'Газова уредба', 'Газова уредба']
#godina 0 = bez znachenie
searches.append({'search_name':'X5_2006',
            'kategoria':'Джипове', 'marka': 'BMW', 
            'model':'X5', 'dvigatel':'Дизелов',
            'godina':[2007, 2007], 'region':'', 'grad':'',
            'opcii':[]})
searches.append({'search_name':'X5_2006',
            'kategoria':'Джипове', 'marka': 'BMW', 
            'model':'X5', 'dvigatel':'Дизелов',
            'godina':[2008, 2008], 'region':'', 'grad':'',
            'opcii':[]})
# searches.append({'search_name':'Skoda',
            # 'kategoria':'Автомобили', 'marka': 'Skoda', 
            # 'model':'Superb', 'dvigatel':'Дизелов',
            # 'godina':[2009, 2013], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'S2006_1',
            # 'kategoria':'Автомобили', 'marka': 'Mercedes-Benz', 
            # 'model':'S', 'dvigatel':'Дизелов',
            # 'godina':[2006, 2009], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'S2006_2',
            # 'kategoria':'Автомобили', 'marka': 'Mercedes-Benz', 
            # 'model':'S', 'dvigatel':'Дизелов',
            # 'godina':[2010, 2013], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'X5',
            # 'kategoria':'Джипове', 'marka': 'BMW', 
            # 'model':'X5', 'dvigatel':'Дизелов',
            # 'godina':[2007,2007], 'region':'София', 'grad':'гр. София',
            # 'opcii':[]})
# searches.append({'search_name':'X5_2003',
            # 'kategoria':'Джипове', 'marka': 'BMW', 
            # 'model':'X5', 'dvigatel':'Дизелов',
            # 'godina':[0, 2003], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'X5_2006',
            # 'kategoria':'Джипове', 'marka': 'BMW', 
            # 'model':'X5', 'dvigatel':'Дизелов',
            # 'godina':[2004, 2006], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'X5_2010',
            # 'kategoria':'Джипове', 'marka': 'BMW', 
            # 'model':'X5', 'dvigatel':'Дизелов',
            # 'godina':[2007, 2010], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'X5_2014',
            # 'kategoria':'Джипове', 'marka': 'BMW', 
            # 'model':'X5', 'dvigatel':'Дизелов',
            # 'godina':[2011, 2014], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'X5_2017',
            # 'kategoria':'Джипове', 'marka': 'BMW', 
            # 'model':'X5', 'dvigatel':'Дизелов',
            # 'godina':[2015, 0], 'region':'', 'grad':'',
            # 'opcii':[]})
# searches.append({'search_name':'MB',
            # 'kategoria':'Джипове', 'marka': 'Mercedes-Benz', 
            # 'model':'', 'dvigatel':'Дизелов',
            # 'godina':[2006,2007], 'region':'София', 'grad':'гр. София',
            # 'opcii':['4x4', 'Парктроник', 'Газова уредба', 'Газова уредба']})

def get_advs_hrefs(browser):
    #get elements
    elems = browser.find_by_tag("a")
    advs = []
    pages = []
    homepage = ''
    #get all pages
    for e in elems:
        href = e['href']
        if ('cgi?act=3' in href and href not in pages):
            pages.append(href)
    for i in range(len(pages)):
        if pages[i][-1] == '#':
            pages[i] = pages[i][:-1]
            homepage = pages[i]
    #print(pages)
    #assert len(pages) <= 10, "Too many results, specify more criteria"
    #check if we are on the first page in the list and 
    #   if not, make the first page the homepage
    #   if not, make the first page the homepage
    if pages[0] != homepage:
        homepage = pages[0]
    #cycle through all pages to get references for advs
    for p in pages:
        if p != homepage:
            browser.visit(p)
        elems = browser.find_by_tag("a")
        for e in elems:
            href = e['href']
            if ('&adv' in href and 'player' not in href and href not in advs):
                advs.append(href)
    browser.visit(homepage)
    #print(len(advs))
    return advs
    
def search_advs(searches):
    browser = Browser()
    advs_dict = {}
    for s in searches:
        browser.visit('http://mobile.bg')
        try:
            browser.find_by_id('ZaplataFooterClose').first.click()
        except Exception as e:
            pass
        browser.find_option_by_text(s['kategoria']).first.click()
        browser.find_option_by_text(s['marka']).first.click()
        if s['model'] != '':
            browser.find_option_by_text(s['model']).first.click()
        #go to Podrobno Tursene
        browser.find_by_text('Подробно търсене').first.click()
        time.sleep(sleep_time)
        #close zaplata banner
        try:
            browser.find_by_id('ZaplataFooterClose').first.click()
            print(1)
        except Exception as e:
            pass
            #print ('could not close banner:', e)
        browser.find_option_by_text(sortirane).first.click()
        if s['dvigatel'] != '':
            browser.find_option_by_text(s['dvigatel']).first.click()
        if s['godina'][0] != 0:
            browser.find_option_by_text('от ' + str(s['godina'][0]) + ' г.').first.click()
        if s['godina'][1] != 0:
            browser.find_option_by_text('до ' + str(s['godina'][1]) + ' г.').first.click()
        if s['region'] != '':
            browser.find_option_by_text(s['region']).first.click()
        if s['grad'] != '':
            browser.find_option_by_text(s['grad']).first.click()
        for o in s['opcii']:
            browser.find_by_text(o).first.click()

        #TODO: add option za chastni obqvi / vsichki obqvi
        browser.find_by_value('Т Ъ Р С И').first.click()
           
        advs = get_advs_hrefs(browser)
        #for h in advs:
        #    print(h)
        print('total', len(advs))
        advs_dict[s['search_name']] = advs
    browser.quit()
    return advs_dict
    
def scrape_ekstri(dict_of_hrefs):
    temp_dict_extri = {}
    for s in dict_of_hrefs.keys():
        counter = 0
        for link in dict_of_hrefs[s]:
            with urllib.request.urlopen(link) as resp:
                html = resp.read()                
            soup = BeautifulSoup(html, 'html.parser')
            #t = (soup.prettify())
            name = soup.title.string
            trs = soup.find_all('tr')
            ekstri = trs[41].text
            temp_dict_extri[name] = ekstri
            #pickle pickle
            pickle_file = open(s + str(counter), 'wb')
            pickle.dump(ekstri, pickle_file)
            counter += 1
            time.sleep(sleep_time)
    return temp_dict_extri
    
def get_cena_proizvodstvo_publikuvane(dict_of_hrefs):
    dict_cena_godina = {}
    for s in dict_of_hrefs.keys():
        counter = 0
        dict_cena_godina[s] = {}
        for link in dict_of_hrefs[s]:
            with urllib.request.urlopen(link) as resp:
                html = resp.read()                
            soup = BeautifulSoup(html, 'html.parser')
            #t = (soup.prettify())
            name = soup.title.string
            trs = soup.find_all('tr')    
            # Find correct indexers - e.g. search for Цена, Дата на производство, Публикувана / Коригирана на...
            cena_t = []
            proizv_t = []
            publ_t = []
            for tr in trs:
                if tr.text.strip()[:5] == 'Цена\n':
                    cena_t = tr.text.split()
                elif tr.text.strip()[:4] == 'Дата':
                    proizv_t = tr.text.split()
                elif tr.text.strip()[:11] == 'Публикувана' or tr.text.strip()[:10] == 'Коригирана':
                    publ_t = tr.text.split()   
            #get cena
            cena = ''
            proizv_mesec = ''
            proizv_godina = ''
            publ_den = ''
            publ_mesec = ''
            publ_godina = ''
            if len(cena_t) > 0:
                try:
                    cena = int(cena_t[1]+cena_t[2])                      
                    if cena_t[3] != 'лв.':
                        cena = 1.958*cena
                except Exception as e:
                    print(e, cena_t)
            #get proizv date
            if len(proizv_t) > 0:
                proizv_mesec = meseci_dict[proizv_t[2][12:]]
                proizv_godina = proizv_t[3]
            #get publikuvana data
            if len(publ_t) > 0:
                idx = publ_t.index('на')
                publ_den = publ_t[idx+1]
                publ_mesec = meseci_dict[publ_t[idx+2].rstrip(',')]
                publ_godina = publ_t[idx+3]          
            dict_cena_godina[s][counter] = [cena, proizv_mesec, proizv_godina, publ_den, publ_mesec, publ_godina]
            counter += 1
    return dict_cena_godina

    
dict_of_hrefs = search_advs(searches)
#print(hr_d)
#scrape_ekstri(dict_of_hrefs)
info = get_cena_proizvodstvo_publikuvane(dict_of_hrefs)
for search in info.keys():
    #print(search)
    with open(search + '.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in info[search].keys():
            l = [search, i] + info[search][i]
            csv_writer.writerow(l)
            #print(i, info[search][i])
    

    
'''
import pandas as pd
import statsmodels.formula.api as sm
data = pandas.read_csv('BMW_f.csv')
data_b = data[['price', 'man', 'up']]
#correlation
c = data_b.corr()
#linear regr
result = sm.ols(formula="price ~ man + up", data=data_b).fit()
print result.summary()
                            # # # OLS Regression Results
# # # ==============================================================================
# # # Dep. Variable:                  price   R-squared:                       0.092
# # # Model:                            OLS   Adj. R-squared:                  0.081
# # # Method:                 Least Squares   F-statistic:                     8.695
# # # Date:                Tue, 08 Aug 2017   Prob (F-statistic):           0.000253
# # # Time:                        16:49:32   Log-Likelihood:                -1698.6
# # # No. Observations:                 175   AIC:                             3403.
# # # Df Residuals:                     172   BIC:                             3413.
# # # Df Model:                           2
# # # Covariance Type:            nonrobust
# # # ==============================================================================
                 # # # coef    std err          t      P>|t|      [95.0% Conf. Int.]
# # # ------------------------------------------------------------------------------
# # # Intercept   2.743e+04    742.502     36.948      0.000       2.6e+04  2.89e+04
# # # man          124.0713     35.074      3.537      0.001        54.840   193.303
# # # up           -22.2599     10.632     -2.094      0.038       -43.246    -1.274
# # # ==============================================================================
# # # Omnibus:                        2.248   Durbin-Watson:                   1.461
# # # Prob(Omnibus):                  0.325   Jarque-Bera (JB):                2.051
# # # Skew:                           0.265   Prob(JB):                        0.359
# # # Kurtosis:                       3.024   Cond. No.                         79.8
# # # ==============================================================================

'''
