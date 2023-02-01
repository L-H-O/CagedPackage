# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:58:52 2023

@author: lider
"""

import os
import sys; sys.path.append(os.path.join(os.getcwd(),"Scrapings"))
import dateparser as dp
import pandas as pd

from cagedlib_scraper import Scraper

#%%
class Cleaner():
    
    def __init__(self, root = None, home = os.getcwd(), data = None):
        
        self.home = home               
        
        try:
            
            os.mkdir(os.path.join(self.home,'raw_caged'))
            self.root = os.path.join(self.home, 'raw_caged')  
            
        except FileExistsError:  
            
            self.root = os.path.join(self.home, 'raw_caged')
            
        try:     
            
           self.data = os.path.join(self.root, os.listdir(self.root)[0]) 
           
        except FileNotFoundError():
           
           Scraper.scrap_caged(update = True)
           self.data = os.path.join(self.root, os.listdir(self.root)[0])
                        
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
            
            return df
        
        else:
            
            return pd.read_excel(pd.read_pickle(os.path.join(self.root, self.data)), sheet_name = str(sheet_name), index_col = 1)
        
#%%        
            
cl = Cleaner().clean_sheet     



        
        


