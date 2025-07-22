from datetime import datetime as dt

import pandas as pd 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import yfinance as yf

class data:
    
    def __init__(self):
        print("criado")
    
    def get_data_ticker(self, ticker, data_inicio = None, data_fim = None):
        self.data_inicio = dt.now().date() if data_inicio == None else data_inicio
        self.data_fim = dt.now().date() if data_fim == None else data_fim
        
        try:
            try:
                service = Service()  
                options = Options()
                options.add_argument('--ignore-certificate-errors')  
                options.add_argument('--start-maximized')           
                options.set_preference("dom.webnotifications.enabled", False)
                driver = webdriver.Firefox(service=service, options=options)
                url_base = f'https://finance.yahoo.com/quote/{ticker}/history/'
                
                driver.get(url_base)
                tabela = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/section/section/section/article/div[1]/div[3]/table'))
                )
                print("Tabela carregada com sucesso!")
                
                try:
                    # Extrair nomes das colunas
                    colunas_th = tabela.find_elements(By.CSS_SELECTOR, 'thead th')
                    cabecalhos = [coluna.text for  coluna in colunas_th]
                    # Extrair primeira linha de dados (após cabeçalho)
                    primeira_linha = tabela.find_element(By.CSS_SELECTOR, 'tbody tr')
                    celulas = primeira_linha.find_elements(By.TAG_NAME, 'td')
                    dados_linha = [celula.text for celula in celulas]
                    
                    df = pd.DataFrame([dados_linha], columns=cabecalhos)
                    df['Ticker'] = ticker
                    return df
                except Exception as e:
                    print("Erro ao processar a linha da tabela: ")
            
            except Exception as e:
                print("Erro ao carregar a tabela:", e)

        except:
            driver.quit()
            df = yf.download(ticker, start=self.data_inicio, end=self.data_fim)
            df['Ticker'] = ticker
            df.columns = df.columns.get_level_values(0)
            return df
        finally:
            driver.quit()