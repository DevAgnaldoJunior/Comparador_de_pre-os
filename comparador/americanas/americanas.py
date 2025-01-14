from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import streamlit as st
import pandas as pd

# Função para inicializar o driver do Selenium
def init_driver():
    options = Options()
    #options.headless = False  #para não abrir o navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Função para buscar produtos
def buscar_produtos(produto_name):
    url_base = "https://www.americanas.com.br/busca/"
    
    driver = init_driver()
    driver.get(url_base + produto_name)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Espera um pouco para garantir que o conteúdo seja carregado
    time.sleep(3) 

    # Obter o HTML da página carregada
    site = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()  # Fechar o navegador após a requisição

    # Agora, continue com o mesmo processo de extração de dados com BeautifulSoup
    produtos = site.find_all('div', attrs={'class': "src__Wrapper-sc-1l8mow4-0"})

    lista_produtos = []

    for produto in produtos:
        nome_do_produto = produto.find('h3')
        if nome_do_produto is None:
            nome_do_produto = produto.select_one('product-name')


        # Link do produto
        link_tag = produto.find('a', href=True)
        link = link_tag['href'] if link_tag else None

        # Certifique-se de que o link não seja nulo e que esteja completo
        if link and not link.startswith('http'):
            link = f'https://www.americanas.com.br{link}'

        # Preço
        preco = produto.find('span', attrs={'class': 'src__Text-sc-154pg0p-0'})

        if preco:  # Verifica se o preço foi encontrado
            preco_texto = preco.text.strip()  # Obtém o texto do preço
            preco_limpo = preco_texto.replace('R$', '').replace('.', '').replace(',', '.').strip()  # Limpeza
            try:
                preco_value = float(preco_limpo)  # Tenta converter para float
            except ValueError:
                preco_value = None  # Se não conseguir converter, atribui None
        else:
            preco_value = None  # Se não encontrar o preço, atribui None

        lista_produtos.append([ 
            nome_do_produto.text.strip() if nome_do_produto else "Nome não disponivel",
            link,
            preco_value
        ])

    return lista_produtos


