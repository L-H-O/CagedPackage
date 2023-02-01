# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 09:04:48 2023

@author: lider
"""
import requests as re
import os
import pickle

from bs4 import BeautifulSoup

#%%  
class Scraper():
    
    def __init__(self, root = None, home = os.getcwd(), url = "http://pdet.mte.gov.br/novo-caged"
                 , aux = "http://pdet.mte.gov.br", name = 'Caged'):
        
        self.home = home
        self.url = url
        self.aux = aux
        self.name = name
          
        try:
            
            os.mkdir(os.path.join(self.home,'raw_caged'))
            self.root = os.path.join(self.home, 'raw_caged')  
            
        except FileExistsError:  
            
            self.root = os.path.join(self.home, 'raw_caged')
            
    def scrap_caged(self, update = False):
        
        if update == True:
            
            self.clear_root()
            self.create_root()
            
            link = re.get(self.url, verify = False)

            soup = BeautifulSoup(link.content, 'html.parser')

            link1 = soup.find_all('ul', class_ = 'n5' )[0].find_all('a')[2]['href']

            finallink = self.aux + link1
        
            data = re.get(finallink).content
        
            return self._dumper(self.name, data)
        
        else:
            
            if len(os.listdir(self.root)) > 0:
                
                print('Dados brutos existentes não foram atualizados')
                
            else:
                
                print('Não constam dados no diretório, raspando...')
                self.scrap_caged(True)
                               
    def _dumper(self, filename, filecontent):
                    
        with open(os.path.join(self.root, filename + '.pickle'), 'wb') as handle:
                
                return pickle.dump(filecontent, handle)
                                
    def clear_root(self, rmdir = False):
        
        if rmdir == False:
            
            root_data = os.listdir(self.root)
            
            [os.remove(os.path.join(self.root, i)) for i in root_data]
        
        else:
        
            try:
        
                os.rmdir(self.root)
        
            except OSError:
            
                aux = os.listdir(self.root)
            
                [os.remove(os.path.join(self.root,i)) for i in aux]
            
                os.rmdir(self.root)
                            
    def create_root(self):
        
        try:
            
            os.mkdir(os.path.join(self.home,'raw_caged'))
            self.root = os.path.join(self.home, 'raw_caged')  
            
        except FileExistsError:  
            pass            
