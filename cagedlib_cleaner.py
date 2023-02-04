# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:58:52 2023

@author: lider
"""
import os
import dateparser as dp
import pandas as pd

from cagedlib_scraper import Scraper
from pandas.tseries.offsets import DateOffset

#%%
class Cleaner:
    
    def __init__(self, root = None, home = os.getcwd(), data = None):
        

        self.home = os.path.dirname(os.path.abspath(Scraper().root)) 
        s = Scraper().scrap_caged             
        
        try:
                                  
            os.mkdir(os.path.join(self.home,'raw_caged'))
            self.root = os.path.join(self.home, 'raw_caged') 
            
            print('Creating root directory...')
            
        except FileExistsError:  
            
            print('Existing root directory detected, checking for raw data...')
            
            self.root = os.path.join(self.home, 'raw_caged')
            
        try:     
                                    
           self.data = os.path.join(self.root, os.listdir(self.root)[0]) 
           
           print('Raw data detected, function is ready')
           
        except FileNotFoundError:
            
            print('No existing raw data detected, scraping...')
           
            s(update = True)                      
            self.data = os.path.join(self.root, os.listdir(self.root)[0])
           
        except IndexError:
            
            print('No existing raw data detected, scraping...')
            
            s(update = True)                      
            self.data = os.path.join(self.root, os.listdir(self.root)[0])
            
        print('Function is ready')    
                                                                                                
    def clean_sheet(self, sheet_name):
                                               
        if sheet_name == 'Tabela 1':
           
            df = pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)
            df = df.iloc[3:,1:]
            df.columns = df.iloc[0,:]
            idx = list(df.index)
            idx[1] = 'Grupamento de Atividades Econômicas e Seção CNAE 2.0'        
            df.index = idx  
            df.index.name = 'Atividades'
            df = df.iloc[1:,:]      
            df.dropna(inplace = True)
            
            dates = df.columns[0].split('-')
            date = dp.parse(dates[0]).strftime("%b-%y")

            cols = list(df.iloc[0,:])
            cols[0] = date +' '+ cols[0]
            df.columns = cols
            df = df.iloc[1:,:]
            
            cols = list(df.columns)
            ncols = [i[1] + ' - com ajuste' for i in enumerate(cols) if i[0] > 3]
            cols[4:9] = ncols
            df.columns = cols
            
            return df
        
        elif sheet_name == 'Tabela 2':
                        
            df = pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)  
            df = df.iloc[3:,:]
            df.columns = df.iloc[0,:]
            idx = list(df.index)
            idx[1] = 'Regiaõ e UF'
            df.index = idx
            df.index.name = 'Nível Territorial'
            df = df.iloc[1:,1:]
            df.dropna(inplace = True)
            
            dates = df.columns[0].split('-')
            date = dp.parse(dates[0]).strftime("%b-%y")

            cols = list(df.iloc[0,:])
            cols[0] = date +' '+ cols[0]
            df.columns = cols
            df = df.iloc[1:,:]

            cols = list(df.columns)
            ncols = [i[1] + ' - acumulado' for i in enumerate(cols) if i[0] > 3]
            cols[4:9] = ncols
            df.columns = cols
            
            return df
        
        elif sheet_name == 'Tabela 3':
                       
            df = pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)
            df = df.iloc[3:,1:]
            df.columns = df.iloc[0,:]
            df.drop(df.index[1:3], inplace = True)
            df = df.iloc[1:,:]         
            df.index.name = 'UF'
            df.dropna(inplace = True)
            
            dates = df.columns[2].split('-')
            date = dp.parse(dates[0]).strftime("%b-%y")

            df.columns = ['Código do Município', 'Município', date + ' Admissões',
                          'Desligamentos', 'Saldo', '(%)', 'Admissões - com ajuste', 'Desligamentos - com ajuste',
                          'Saldo - com ajuste', '(%) - com ajuste']
            
            return df    
        
        elif sheet_name == 'Tabela 4':
            
            df = pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)
            df = df.iloc[4:,1:]
            df.columns = df.iloc[0,:]
            df = df.iloc[1:,:]
            df.dropna(inplace = True)
            
            return df
        
        elif sheet_name == 'Tabela 5' or sheet_name == 'Tabela 5.1':
            
            df = pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)
            df = df.iloc[3:,1:]
            df.columns = df.iloc[0,:]
            df.dropna(inplace = True)
            df.index = pd.Series(df.index).apply(lambda x: dp.parse(x))
            df.index.name = 'Date'
            df = df.iloc[1:,:]
            
            return df
        
        elif sheet_name == 'Tabela 6' or sheet_name == 'Tabela 6.1':
            
            df = pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)
            df = df.iloc[3:,:-4]
            
            x = df.T
            x.iloc[:,0] = x.iloc[:,0].ffill()
            x = x.iloc[1:]
            x.index = x.iloc[:,0] = x.iloc[:,0].apply(lambda x : dp.parse(x))
            x.index.name = 'Date'
            x = x.iloc[:,1:]
            x.rename(columns = {x.columns[0]:'Setor'}, inplace = True)
            
            df = x.T
            df.dropna(inplace = True)
            df = df.T
            
            return df
        
        elif sheet_name == 'Tabela 9':
            
            df = pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name),    header = 4, parse_dates = ['Mês'])
            df = df.iloc[:,1:]
            df.dropna(inplace = True)
            
            df.Mês = pd.to_datetime(df.Mês.apply(lambda x: dp.parse(x)))
            df.set_index(df.Mês, inplace = True)
            df.drop(columns = "Mês", inplace = True)

            df.index = df.index.where(~df.index.duplicated(), df[df.index.duplicated()].index[0] + DateOffset(months = 1))
            df.index.name = 'Date'
            df = df.resample('M').last()
            
            return df
        
        else:
            
            return pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)
        
        
    def load(self, series, update = False):
            
        l = self.clean_sheet
        
        if update == True:
            
            print('Updating and cleaning data...')
            s = Scraper().scrap_caged     
            s(update = True)   
                               
        else: 
            
            print('Cleaning data...')   
        
        if type(series) == list and len(series) > 1:
        
            return list(map(l, series))
        
        elif type(series) == list:
                                    
            series = str(series[0])
            
            return l(series)
                
        else: 
            
            series = str(series)
            
            return l(series
            



        
        


