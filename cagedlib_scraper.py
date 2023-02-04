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
class Scraper:
    
    """ 
    Scrapes New Caged data
    
    """
    
    def __init__(self, root = None, home = os.getcwd(), url = "http://pdet.mte.gov.br/novo-caged"
                 , aux = "http://pdet.mte.gov.br", name = 'Caged'):
        
        """ 
        
        Sets up the the database root and urls to be scraped
        
        :param root: Directory
        :type root: str
        
        :param home: Path
        :type home: str
        
        :param url: Link
        :type url: str
        
        :param aux: Link
        :type aux: str
        
        :param name: Database name
        :type name: str
        
        """
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
        
        """
        
        Scraps caged data
        
        :param update: If True, scrapes new data
        :type update: Boolean 
        
        """
        
        if update == True:
            
            print('Scraping data...')
            
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
                
                print('Existing raw data not updated')
                
            else:
                
                print('No existing raw data detected, scraping...')
                self.scrap_caged(True)
                               
    def _dumper(self, filename, filecontent):
        
        """
        
        Pickles and dumps the data into the root directory
        
        :param filename: Name of the file
        :type filename: str
        
        :param filecontent: Content of the file
        :type filecontent: bytes
        
        """
                    
        with open(os.path.join(self.root, filename + '.pickle'), 'wb') as handle:
                
                return pickle.dump(filecontent, handle)
                                
    def clear_root(self, rmdir = False):
        
        """ 
        Auxiliar function that cleans the root if an update is requested
        
        :param rmdir: Removes root if called
        :type rmdir: Boolean
        
        """
        
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
        
        """
        Auxiliar function that creates root if upddate is called
        
        """
        
        try:
            
            os.mkdir(os.path.join(self.home,'raw_caged'))
            self.root = os.path.join(self.home, 'raw_caged')  
            
        except FileExistsError:  
            pass           
